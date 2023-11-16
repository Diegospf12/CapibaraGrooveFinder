from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import time

from knn_highD import knn_search_faiss
from knn_rtree import knn_search_rtree
from knn_secuencial import knn_search, range_search
from feature_extraction import feature_extraction, query_feature_extraction

#uvicorn api:app --reload
#source venv/bin/activate
app = FastAPI()

# Configura las credenciales de la API de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="22fced1f18674a96988152d2866af53c", client_secret="06d02e123c974506be3fabd5f44d7745"))

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/search')
async def search(k: int, file: UploadFile = File(...)):
    # Lee el archivo de audio y extrae las características
    audio_data = await file.read()
    query_vector = query_feature_extraction(audio_data)

    # Realiza la búsqueda de los vecinos más cercanos
    start = time.time()
    nearest_neighbors = knn_search_rtree(query_vector, k)    
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