import numpy as np
import faiss
import psycopg2
from feature_extraction import feature_extraction
import time

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def create_index():
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS index_table (
        id SERIAL PRIMARY KEY,
        index_blob BYTEA
    )
    """)

    cur.execute("SELECT track_id, mfcc FROM vectores")
    features = {row[0]: row[1] for row in cur.fetchall()}

    feature_matrix = np.array([feature_vector for feature_vector in features.values()]).astype('float32')

    quantizer = faiss.IndexFlatL2(feature_matrix.shape[1])
    index = faiss.IndexIVFFlat(quantizer, feature_matrix.shape[1], 3)

    assert not index.is_trained
    index.train(feature_matrix)
    assert index.is_trained

    index.add(feature_matrix)

    faiss.write_index(index, 'index_file')

    with open('index_file', 'rb') as f:
        index_blob = f.read()

    cur.execute("INSERT INTO index_table (index_blob) VALUES (%s)", (psycopg2.Binary(index_blob),))

    conn.commit()

    cur.close()
    conn.close()


conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

cur.execute("SELECT track_id, mfcc FROM vectores")
features = {row[0]: row[1] for row in cur.fetchall()}

cur.execute("SELECT index_blob FROM index_table ORDER BY id DESC LIMIT 1")
index_blob = cur.fetchone()[0]

cur.close()
conn.close()

with open('index_file', 'wb') as f:
    f.write(index_blob)

def knn_search_faiss(query_vector, K):
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    index = faiss.read_index('index_file')

    query_matrix = np.array([query_vector]).astype('float32')
    
    distances, indices = index.search(query_matrix, K)
    
    nearest_neighbors = [(list(features.keys())[indices[0][i]], distances[0][i]) for i in range(K)]
    
    cur.close()
    conn.close()

    return nearest_neighbors

'''
query = feature_extraction("/Users/diegopachecoferrel/Desktop/MultimediaIndex/tracks/0FZ4Dmg8jJJAPJnvBIzD9z.wav")
query_vector = query  # Reemplaza esto con tu vector de consulta real
K = 5  # Reemplaza esto con el número de vecinos más cercanos que quieres encontrar

nearest_neighbors = knn_search_faiss(query_vector, K)

for audio_path, distance in nearest_neighbors:
    print(f'Audio path: {audio_path}, Distance: {distance}')
'''