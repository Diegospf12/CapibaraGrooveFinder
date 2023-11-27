import os
import librosa
import psycopg2
from psycopg2 import sql
import wave
import numpy as np
import tempfile

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


# Función para extraer características MFCC
def feature_extraction(file_path):
    with wave.open(file_path, 'rb') as wave_file:
        sample_rate = wave_file.getframerate()
        data = np.frombuffer(wave_file.readframes(wave_file.getnframes()), dtype=np.int16)

    if data.size == 0:
        return None
    
    data = data.astype(np.float32)
    
    mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=50).T, axis=0)
    
    return mfcc


def query_feature_extraction(audio_data: bytes):
    with tempfile.NamedTemporaryFile(delete=True) as temp_audio:
        temp_audio.write(audio_data)
        temp_audio.flush()

        with wave.open(temp_audio.name, 'rb') as wave_file:
            sample_rate = wave_file.getframerate()
            data = np.frombuffer(wave_file.readframes(wave_file.getnframes()), dtype=np.int16)
    
        data = data.astype(np.float32)
    
        mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=50).T, axis=0)
    
        return mfcc

'''
# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

# Crea la tabla
create_table_query = """
CREATE TABLE IF NOT EXISTS songs (
    track_id TEXT PRIMARY KEY,
    mfcc float[]
)
"""
cur.execute(create_table_query)


# Recorre todos los archivos .mp3 en el directorio
for file_name in os.listdir('/Users/diegopachecoferrel/Desktop/MultimediaIndex/tracks/'):
    if file_name.endswith('.wav'):
        # Extrae las características MFCC
        mfcc = feature_extraction('/Users/diegopachecoferrel/Desktop/MultimediaIndex/tracks/' + file_name)
        # Si mfcc es None, saltar la inserción en la base de datos
        if mfcc is None:
            continue
        # Extrae el track_id del nombre del archivo
        track_id = os.path.splitext(file_name)[0]
        # Inserta el track_id y las características MFCC en la base de datos
        insert = sql.SQL("INSERT INTO songs (track_id, mfcc) VALUES (%s, %s)")
        # Convierte los datos de numpy.float32 a float antes de insertarlos
        cur.execute(insert, (track_id, [float(x) for x in mfcc.flatten()]))


# Cierra la conexión a la base de datos
conn.commit()
cur.close()
conn.close()
'''
