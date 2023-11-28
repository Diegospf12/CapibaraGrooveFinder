from rtree import index
import numpy as np
from scipy.spatial import distance
import psycopg2
from feature_extraction import feature_extraction
import time

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

cur.execute("SELECT track_id, mfcc FROM vectores")
features = {row[0]: row[1] for row in cur.fetchall()}

p = index.Property()
p.dimension = len(next(iter(features.values())))
idx = index.Index(properties=p)

objects = []
for i, (audio_path, feature_vector) in enumerate(features.items()):
    idx.insert(i, np.concatenate([feature_vector, feature_vector]))
    objects.append(audio_path)

cur.close()
conn.close()

def knn_search_rtree(query_vector, K):
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    nearest_neighbors = list(idx.nearest(np.concatenate([query_vector, query_vector]), K))
    
    nearest_neighbors = [(objects[i], distance.euclidean(query_vector, features[objects[i]])) for i in nearest_neighbors]

    cur.close()
    conn.close()

    return nearest_neighbors


'''
query = feature_extraction("/Users/diegopachecoferrel/Desktop/MultimediaIndex/tracks/0tCUHZZmlErTi6LyjdS0zU.wav")
query_vector = query  # Reemplaza esto con tu vector de consulta real
K = 5  # Reemplaza esto con el número de vecinos más cercanos que quieres encontrar

nearest_neighbors = knn_search_rtree(query_vector, K)

for audio_path, distance in nearest_neighbors:
    print(f'Audio path: {audio_path}, Distance: {distance}')
'''