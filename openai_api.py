import openai
import tiktoken
from db import conn

def get_api_key():
    cursor = conn.cursor()

    query = "SELECT value FROM utilities WHERE name = 'OpenAIAPIKey';"

    cursor.execute(query)
    result = cursor.fetchone()

    api_key = result[0] if result else None

    cursor.close()

    return api_key

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def video_summarize(captions, video_details):
    openai.api_key = get_api_key()

    prompt = f"This is the main info about a YouTube video. Title: {video_details['title']}. Category: {video_details['category']}. Main tags: {video_details['tags']}. Transcription: {captions}. I want just a json like this:  {{\"main_ideas\": extract the main ideas in separate sentences beggining with an emoji as strings in an array,\"summary\": give me a summary of the video (without writing explicitly the tags and the category that a I give you), \"sentiment_analysis\": sentiment analysys of the video in one sentence, \"category\": recategorize if you consider necessary if not the same category}}. All in the transcription language"

    # Split the prompt into chunks
    word_limit = 2000
    words = prompt.split()
    chunks = [words[i:i+word_limit] for i in range(0, len(words), word_limit)]
    messages = [{"role": "user", "content": ' '.join(chunk)} for chunk in chunks]

    print(len(prompt))
    # print(num_tokens_from_messages(messages))
    print(num_tokens_from_string(prompt, "p50k_base"))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3,
        frequency_penalty=0.5,
        presence_penalty=0,
        max_tokens=4096-num_tokens_from_messages(messages), # 4096 is the max token limit fro gpt 3.5
    )
    return response['choices'][0]['message']['content']
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=prompt,
    #     temperature=0.5,
    #     frequency_penalty=0.5,
    #     presence_penalty=0,
    #     max_tokens=4096-num_tokens_from_string(prompt,"p50k_base"), # 4096 is the max token limit fro gpt 3.5
    # )
    # return response['choices'][0]['text']