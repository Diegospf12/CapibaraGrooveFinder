import psycopg2
import pandas as pd

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def create():
    # Conecta a la base de datos
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
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


def create_inverted_index_table():
    # Conecta a la base de datos
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    # Crea la tabla de índice invertido
    cur.execute("""
    CREATE TABLE IF NOT EXISTS inverted_index (
        track_id TEXT PRIMARY KEY,
        metadata TSVECTOR
    )
    """)

    # Crea un índice GIN en el campo metadata para acelerar las consultas
    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_gin_metadata ON inverted_index USING gin(metadata)
    """)

    # Lee cada registro de la tabla spotify_songs
    cur.execute("SELECT track_id, track_name, track_artist, lyrics, track_album_name, playlist_genre, playlist_subgenre FROM spotify_songs")
    records = cur.fetchall()

    # Inserta cada registro en la tabla inverted_index
    for record in records:
        track_id = record[0]
        metadata = ' '.join(map(str, record[1:]))
        cur.execute("""
        INSERT INTO inverted_index (track_id, metadata) VALUES (%s, to_tsvector(%s))
        """, (track_id, metadata))

    # No olvides hacer commit de la transacción
    conn.commit()

    # Cierra la conexión a la base de datos
    cur.close()
    conn.close()

#create_inverted_index_table()