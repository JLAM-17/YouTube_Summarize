from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from db import conn
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

def get_api_key():
    cursor = conn.cursor()

    query = "SELECT value FROM utilities WHERE name = 'YouTubeAPIKey';"

    cursor.execute(query)
    result = cursor.fetchone()

    api_key = result[0] if result else None

    cursor.close()

    return api_key


# Extract the video ID from the YouTube video link
def extract_video_id(video_link):
    # You can use a regular expression or string manipulation techniques
    # Here's an example using string manipulation assuming the video link is in the format: https://www.youtube.com/watch?v=VIDEO_ID
    video_id = video_link.split('v=')[1]
    if '&' in video_id:
        video_id = video_id.split('&')[0]

    return video_id

def get_video_details(video_id):
    # Create a service object for interacting with the YouTube Data API
    api_key = get_api_key()
    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()
        if (request["items"][0]["snippet"]["categoryId"] != ""):
            category = youtube.videoCategories().list(
                part="snippet",
                id=request["items"][0]["snippet"]["categoryId"]
            ).execute()
            category = category["items"][0]["snippet"]["title"]
        
        tags = request["items"][0]["snippet"].get("tags", [])
        if not tags:  # Check if tags list is empty
            tags = ["No tags available"] 

        response = {
            "title": request["items"][0]["snippet"]["title"],
            "channel": request["items"][0]["snippet"]["channelTitle"],
            "cover": request["items"][0]["snippet"]["thumbnails"]["high"]["url"],
            "tags": tags[:5],
            "category": category,
            "defaultLanguage": request["items"][0]["snippet"].get("defaultAudioLanguage", "en"),
        }
        return response
    except HttpError as e:
        return jsonify({'error': str(e)}), 500
    

def get_captions(video_id,language):
    try:
        captions = YouTubeTranscriptApi.get_transcript(video_id,preserve_formatting=True,languages = [language,"en","es","pt"])
    except:
        captions = "error"
        print("ERROR")
    return captions
    
