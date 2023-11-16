import heapq
from scipy.spatial import distance
import psycopg2
from feature_extraction import feature_extraction

def knn_search(query_vector, K):
    # Conecta a la base de datos
    conn = psycopg2.connect(database="postgres", user="postgres", password="1234", host="localhost", port="5432")
    cur = conn.cursor()

    # Obtiene todos los vectores de la base de datos
    cur.execute("SELECT track_id, mfcc FROM songs")
    features = {row[0]: row[1] for row in cur.fetchall()}

    # Calcular la distancia entre el vector de consulta y todos los vectores en features
    distances = [(audio_path, distance.euclidean(query_vector, feature_vector)) for audio_path, feature_vector in features.items()]
    
    # Encontrar los K vectores más cercanos
    nearest_neighbors = heapq.nsmallest(K, distances, key=lambda x: x[1])
    
    # Cierra la conexión a la base de datos
    cur.close()
    conn.close()

    return nearest_neighbors

def range_search(query_vector, radius):
    # Conecta a la base de datos
    conn = psycopg2.connect(database="postgres", user="postgres", password="1234", host="localhost", port="5432")
    cur = conn.cursor()

    # Obtiene todos los vectores de la base de datos
    cur.execute("SELECT track_id, mfcc FROM songs")
    features = {row[0]: row[1] for row in cur.fetchall()}

    # Calcular la distancia entre el vector de consulta y todos los vectores en features
    distances = [(audio_path, distance.euclidean(query_vector, feature_vector)) for audio_path, feature_vector in features.items()]
    
    # Encontrar los vectores dentro del radio de búsqueda
    results = [item for item in distances if item[1] <= radius]
    
    # Cierra la conexión a la base de datos
    cur.close()
    conn.close()

    return results


'''
query = feature_extraction("/Users/diegopachecoferrel/Desktop/MultimediaIndex/tracks/0qBug5X3DaJv2zgXtp55wn.wav")
query_vector = query
radius = 50.0
K = 5

nearest_neighbors = knn_search(query_vector, K)
results = range_search(query_vector, radius)


for track_id, distance in nearest_neighbors:
    print(f'track_id: {track_id}, Distance: {distance}')


for track_id, distance in results:
    print(f'track_id: {track_id}, Distance: {distance}')

'''