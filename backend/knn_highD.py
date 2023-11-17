import numpy as np
import faiss
import psycopg2
from feature_extraction import feature_extraction

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def create_index():
    # Conecta a la base de datos
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    # Crea la tabla si no existe
    cur.execute("""
    CREATE TABLE IF NOT EXISTS index_table (
        id SERIAL PRIMARY KEY,
        index_blob BYTEA
    )
    """)

    # Obtiene todos los vectores de la base de datos
    cur.execute("SELECT track_id, mfcc FROM songs")
    features = {row[0]: row[1] for row in cur.fetchall()}

    # Convertir los vectores de características a una matriz numpy de tipo float32
    feature_matrix = np.array([feature_vector for feature_vector in features.values()]).astype('float32')

    # Crear un índice de búsqueda de los vecinos más cercanos con Faiss
    quantizer = faiss.IndexFlatL2(feature_matrix.shape[1])
    index = faiss.IndexIVFFlat(quantizer, feature_matrix.shape[1], 3)

    # Entrenar el índice
    assert not index.is_trained
    index.train(feature_matrix)
    assert index.is_trained

    # Agregar los vectores de características al índice
    index.add(feature_matrix)

    # Guardar el índice en un archivo
    faiss.write_index(index, 'index_file')

    # Leer el archivo y guardar su contenido en una variable
    with open('index_file', 'rb') as f:
        index_blob = f.read()

    # Guardar el índice en la base de datos
    cur.execute("INSERT INTO index_table (index_blob) VALUES (%s)", (psycopg2.Binary(index_blob),))

    # No olvides hacer commit de la transacción
    conn.commit()

    # Cierra la conexión a la base de datos
    cur.close()
    conn.close()

def knn_search_faiss(query_vector, K):
    # Conecta a la base de datos
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    # Obtiene todos los vectores de la base de datos
    cur.execute("SELECT track_id, mfcc FROM songs")
    features = {row[0]: row[1] for row in cur.fetchall()}

    # Obtener el último índice de la base de datos
    cur.execute("SELECT index_blob FROM index_table ORDER BY id DESC LIMIT 1")
    index_blob = cur.fetchone()[0]

    # Guardar el índice en un archivo
    with open('index_file', 'wb') as f:
        f.write(index_blob)

    # Cargar el índice desde el archivo
    index = faiss.read_index('index_file')

    # Convertir el vector de consulta a una matriz numpy de tipo float32
    query_matrix = np.array([query_vector]).astype('float32')
    
    # Encontrar los K vecinos más cercanos
    distances, indices = index.search(query_matrix, K)
    
    # Recuperar las rutas de los audios y las distancias
    nearest_neighbors = [(list(features.keys())[indices[0][i]], distances[0][i]) for i in range(K)]
    
    # Cierra la conexión a la base de datos
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
