from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import time
from dotenv import load_dotenv
import psycopg2
import re

from knn_highD import knn_search_faiss
from knn_rtree import knn_search_rtree
from knn_secuencial import knn_search, range_search
from feature_extraction import feature_extraction, query_feature_extraction
from spimi import TextRetrival, obtener_abreviatura_idioma
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

#uvicorn api:app --reload
#source venv/bin/activate
app = FastAPI()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/get_k')
async def search(k: int, file: UploadFile = File(...)):
    audio_data = await file.read()
    query_vector = query_feature_extraction(audio_data)

    start = time.time()
    nearest_neighbors = knn_search_faiss(query_vector, k)    
    end = time.time()
    execution_time = end - start

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
async def search(query: str, k: int, option:str):
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    ts_query = re.sub(r'[^a-zA-ZÑñáéíóúÁÉÍÓÚ]', ' ', query)
    ts_query = ts_query.replace(' ', '&')
    ts_query = re.sub(r'&{2,}', '&', ts_query) 
    ts_query = re.sub(r'&$', '', ts_query) 
    ts_query = re.sub(r'^&', '', ts_query) 

    results = []

    start_time = time.time()
    if option == 'postgres':
        cur.execute("""
        SELECT track_id, ts_rank(metadata, to_tsquery(%s)) as score
        FROM inverted_index
        WHERE metadata @@ to_tsquery(%s)
        ORDER BY score DESC
        LIMIT %s
        """, (ts_query, ts_query, k))

        results = cur.fetchall()
    elif option == 'myindex':
        text_retrival = TextRetrival()
        lenguage = obtener_abreviatura_idioma(query)

        results = text_retrival.get_top_k(query, lenguage, k)
    end_time = time.time()

    execution_time = end_time - start_time

    tracks = []
    for track_id, score in results:
        for _ in range(3):
            try:
                track = sp.track(track_id)
                cur.execute("SELECT lyrics, playlist_name, duration_ms, track_album_name  FROM spotify_songs WHERE track_id = %s", (track_id,))
                row = cur.fetchone()
                lyrics = row[0]
                playlist_name = row[1]
                duration_ms = row[2]
                album_name = row[3]
                duration_minutes = duration_ms // 60000
                duration_seconds = (duration_ms % 60000) // 1000
                tracks.append({
                    'id': track_id,
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'preview_url': track['preview_url'],
                    'lyrics' : lyrics,
                    'score': float(score),
                    'url': track['external_urls']['spotify'],
                    'image': track['album']['images'][0]['url'],
                    'playlist_name': playlist_name,
                    'minutes': duration_minutes,
                    'seconds': duration_seconds,
                    'album': album_name
                })
                break
            except requests.exceptions.ReadTimeout:
                continue

    cur.close()
    conn.close()

    return {'tracks': tracks, 'execution_time': execution_time}

@app.get('/get_top_k')
async def get_top_k(track_id: str, k: int):

    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    cur.execute("SELECT mfcc FROM vectores WHERE track_id = %s", (track_id,))

    if cur.rowcount == 0:
        return {'tracks': [], 'execution_time': 0}

    query_vector = cur.fetchone()[0]

    start = time.time()
    nearest_neighbors = knn_search_faiss(query_vector, k+1)  
    nearest_neighbors.pop(0)  
    end = time.time()
    execution_time = end - start

    tracks = []
    for track_id, distance in nearest_neighbors:
        for _ in range(3):
            try:
                track = sp.track(track_id)
                tracks.append({
                    'id': track_id,
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

    cur.close()
    conn.close()

    return {'tracks': tracks, 'execution_time': execution_time}