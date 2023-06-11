import psycopg2

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
