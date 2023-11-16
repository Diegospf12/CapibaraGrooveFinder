import psycopg2
import pandas as pd

# Conecta a la base de datos
conn = psycopg2.connect(database="postgres", user="postgres", password="1234", host="localhost", port="5432")
cur = conn.cursor()

# Crea la tabla
cur.execute("""
CREATE TABLE IF NOT EXISTS spotify_songs (
    track_id TEXT PRIMARY KEY,
    track_name TEXT,
    track_artist TEXT,
    lyrics TEXT,
    track_popularity INTEGER,
    track_album_id TEXT,
    track_album_name TEXT,
    track_album_release_date TEXT,
    playlist_name TEXT,
    playlist_id TEXT,
    playlist_genre TEXT,
    playlist_subgenre TEXT,
    danceability REAL,
    energy REAL,
    key INTEGER,
    loudness REAL,
    mode INTEGER,
    speechiness REAL,
    acousticness REAL,
    instrumentalness REAL,
    liveness REAL,
    valence REAL,
    tempo REAL,
    duration_ms INTEGER,
    language TEXT
)
""")

# Lee el archivo CSV
df = pd.read_csv('spotify_songs.csv', delimiter=',', quotechar='"')

# Inserta los registros en la tabla
for row in df.itertuples(index=False):
    cur.execute("""
    INSERT INTO spotify_songs VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """, row)

# No olvides hacer commit de la transacción
conn.commit()

# Cierra la conexión a la base de datos
cur.close()
conn.close()