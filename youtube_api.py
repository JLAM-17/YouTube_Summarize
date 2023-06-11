from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from db import conn


def get_api_key():
    cursor = conn.cursor()

    query = "SELECT value FROM utilities WHERE name = 'YouTubeAPIKey';"

    cursor.execute(query)
    result = cursor.fetchone()

    api_key = result[0] if result else None

    cursor.close()

    return api_key




# Set up YouTube API
api_service_name = "youtube"
api_version = "v3"
api_key = get_api_key()

youtube = build(api_service_name, api_version, developerKey=api_key)

