from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import time
import os
from dotenv import load_dotenv
import psycopg2

from knn_highD import knn_search_faiss
from knn_rtree import knn_search_rtree
from knn_secuencial import knn_search, range_search
from feature_extraction import feature_extraction, query_feature_extraction
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

#uvicorn api:app --reload
#source venv/bin/activate
app = FastAPI()

# Configura las credenciales de la API de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/get_k')
async def search(k: int, file: UploadFile = File(...)):
    # Lee el archivo de audio y extrae las características
    audio_data = await file.read()
    query_vector = query_feature_extraction(audio_data)

    # Realiza la búsqueda de los vecinos más cercanos
    start = time.time()
    nearest_neighbors = knn_search_faiss(query_vector, k)    
    end = time.time()
    execution_time = end - start

    # Obtiene los detalles de las canciones de la API de Spotify
    tracks = []
    for track_id, distance in nearest_neighbors:
        for _ in range(3):
            try:
                track = sp.track(track_id)
                tracks.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'preview_url': track['preview_url'],
                    'lyrics' : "aqui va la letra",
                    'distance': float(distance),
                    'url': track['external_urls']['spotify'],
                    'image': track['album']['images'][0]['url'] 
                })
                break
            except requests.exceptions.ReadTimeout:
                continue

    return {'tracks': tracks, 'execution_time': execution_time}

@app.get('/search')
async def search(query: str, k: int):
    # Conecta a la base de datos
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    # Reemplaza los espacios en la consulta con el operador '&'
    ts_query = query.replace(' ', ' & ')

    # Realiza la búsqueda en el índice invertido
    cur.execute("""
    SELECT track_id, ts_rank(metadata, to_tsquery(%s)) as score
    FROM inverted_index
    WHERE metadata @@ to_tsquery(%s)
    ORDER BY score DESC
    LIMIT %s
    """, (ts_query, ts_query, k))

    # Obtiene los k track_ids más relevantes
    results = cur.fetchall()

    # Obtiene los detalles de las canciones de la API de Spotify
    tracks = []
    for track_id, score in results:
        for _ in range(3):
            try:
                track = sp.track(track_id)
                cur.execute("SELECT lyrics FROM spotify_songs WHERE track_id = %s", (track_id,))
                lyrics = cur.fetchone()[0]
                tracks.append({
                    'id': track_id,
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'preview_url': track['preview_url'],
                    'lyrics' : lyrics,
                    'score': float(score),
                    'url': track['external_urls']['spotify'],
                    'image': track['album']['images'][0]['url'],
                })
                break
            except requests.exceptions.ReadTimeout:
                continue

    # Cierra la conexión a la base de datos
    cur.close()
    conn.close()

    return {'tracks': tracks}

@app.get('/get_top_k')
async def get_top_k(track_id: str, k: int):
    # Conecta a la base de datos
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    # Obtiene el vector de la canción con el track_id dado
    cur.execute("SELECT mfcc FROM songs WHERE track_id = %s", (track_id,))

    # Verifica si el track_id existe
    if cur.rowcount == 0:
        return {'tracks': [], 'execution_time': 0}

    # Obtiene el vector de características
    query_vector = cur.fetchone()[0]

    # Realiza la búsqueda de los vecinos más cercanos
    start = time.time()
    nearest_neighbors = knn_search_faiss(query_vector, k)    
    end = time.time()
    execution_time = end - start

    # Obtiene los detalles de las canciones de la API de Spotify
    tracks = []
    for track_id, distance in nearest_neighbors:
        for _ in range(3):
            try:
                track = sp.track(track_id)
                tracks.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'preview_url': track['preview_url'],
                    'distance': float(distance),
                    'url': track['external_urls']['spotify'],
                    'image': track['album']['images'][0]['url'] 
                })
                break
            except requests.exceptions.ReadTimeout:
                continue

    # Cierra la conexión a la base de datos
    cur.close()
    conn.close()

    return {'tracks': tracks, 'execution_time': execution_time}