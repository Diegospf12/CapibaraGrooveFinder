from rtree import index
import numpy as np
from scipy.spatial import distance
import psycopg2
from feature_extraction import feature_extraction

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Conecta a la base de datos
conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

# Obtiene todos los vectores de la base de datos
cur.execute("SELECT track_id, mfcc FROM songs")
features = {row[0]: row[1] for row in cur.fetchall()}

# Crear un índice RTree
p = index.Property()
p.dimension = len(next(iter(features.values())))  # Establecer la dimensión a la longitud de los vectores de características
idx = index.Index(properties=p)

# Indexar todos los vectores de características
objects = []
for i, (audio_path, feature_vector) in enumerate(features.items()):
    idx.insert(i, np.concatenate([feature_vector, feature_vector]))
    objects.append(audio_path)

def knn_search_rtree(query_vector, K):
    # Encontrar los K vecinos más cercanos
    nearest_neighbors = list(idx.nearest(np.concatenate([query_vector, query_vector]), K))
    
    # Recuperar las rutas de los audios y las distancias
    nearest_neighbors = [(objects[i], distance.euclidean(query_vector, features[objects[i]])) for i in nearest_neighbors]
    
    # Cierra la conexión a la base de datos
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