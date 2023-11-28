import heapq
from scipy.spatial import distance
import psycopg2
from feature_extraction import feature_extraction
import time

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

cur.execute("SELECT track_id, mfcc FROM vectores")
features = {row[0]: row[1] for row in cur.fetchall()}

cur.close()
conn.close()

def knn_search(query_vector, K):

    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    distances = [(audio_path, distance.euclidean(query_vector, feature_vector)) for audio_path, feature_vector in features.items()]
    
    nearest_neighbors = heapq.nsmallest(K, distances, key=lambda x: x[1])
    
    cur.close()
    conn.close()

    return nearest_neighbors


def range_search(query_vector, radius):

    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    distances = [(audio_path, distance.euclidean(query_vector, feature_vector)) for audio_path, feature_vector in features.items()]
    
    results = [item for item in distances if item[1] <= radius]
    
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