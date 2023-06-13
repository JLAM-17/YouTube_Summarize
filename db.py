import psycopg2
import time
import json
import re


DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'YouTube_Makers'
DB_USER = 'youtube_makers'
DB_PASSWORD = 'rNxE1dSy!QKI#dt26#0n'

# Connect to the database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def generate_video_id(title):
    # Remove special characters from the title
    title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
    # Convert the title to lowercase and replace spaces with hyphens
    title = title.lower().replace(' ', '-')
    # Get the current timestamp as a string
    timestamp = str(time.time()).split('.')[1][:4]
    # Concatenate the title and timestamp
    video_id = f"{title}-{timestamp}"
    return video_id

def insert_video(video_details, summary):
    print(summary)
    summary = json.loads(summary)
    cursor = conn.cursor()
    query = "INSERT INTO videos (video_id,title,channel,cover,tags,category,default_language,main_ideas,summary,sentiment_analysis) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    
    video_id = generate_video_id(video_details["title"])

    cursor.execute(query,(video_id,video_details["title"],video_details["channel"],video_details["cover"],video_details["tags"],video_details["category"],video_details["defaultLanguage"],str(summary["main_ideas"]).replace("'", '').replace("\"", ''),str(summary["summary"]),str(summary["sentiment_analysis"])))
    conn.commit()

    cursor.close()

    return video_id

def get_video_by_id(video_id):
    cursor = conn.cursor()
    query = "SELECT * FROM videos WHERE video_id = %s;"
    cursor.execute(query,(video_id,))
    row = cursor.fetchone()
    # Convert the result into a dictionary
    columns = [desc[0] for desc in cursor.description]
    video = dict(zip(columns, row))
    video["main_ideas"].replace("'", '')
    video["main_ideas"].replace("\"", '')
    print(video["main_ideas"])
    cursor.close()
    return video
