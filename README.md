# **Capibara Groove Finder**
**Proyecto 2 & 3 del curso de Base de datos II. Construcción del índice invertido textual y multidimensional**

# Team - Group 5
| <a href="https://github.com/anamariaaccilio" target="_blank">**Ana Maria Accilio Villanueva**</a> | <a href="https://github.com/Diegospf12" target="_blank">**Diego Pacheco Ferrel**</a> | <a href="https://github.com/juanpedrovv" target="_blank">**Juan Pedro Vasquez Vilchez**</a> | <a href="https://github.com/LuisEnriqueCortijoGonzales" target="_blank">**Luis Enrique Cortijo Gonzales**</a> | <a href="https://github.com/marceloZS" target="_blank">**Marcelo Mario Zuloeta Salazar**</a> |
| :----------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------: |
| <img src="https://avatars.githubusercontent.com/u/91237434?v=4" alt="drawing" width="200"/> | <img src="https://avatars.githubusercontent.com/u/94090499?v=4" alt="drawing" width="200"/> | <img src="https://avatars.githubusercontent.com/u/83739305?v=4" alt="drawing" width="200"/> | <img src="https://avatars.githubusercontent.com/u/84096868?v=4" alt="drawing" width="200"/> | <img src="https://avatars.githubusercontent.com/u/85197213?v=4" alt="drawing" width="200"/> |

<a name="readme-top"></a>
<details open>
  <summary><h2>Tabla de contenidos:<h2></summary>
  <ul>
    <li><a href="#Introducción-🖊">Introducción 🖊
      <ul>
        <li><a href="#objetivo-del-proyecto">Objetivo del proyecto</a></li>
        <li><a href="#Dominio-de-datos">Dominio de datos</a></li>
        <li><a href="#Importacia-de-aplicar-indexación">Importancia de aplicar indexación</a></li>
      </ul>
    </a></li> 
    <li><a href="#Estructura-del-proyecto">Estructura del proyecto</a></li>
    <li><a href="#Backend-(Índice-Invertido)">Backend (Índice Invertido)</a></li>
    <li><a href="#Backend-(Índice-Multidimensional)">Backend (Índice Multidimensional)</a></li>
    <li><a href="#Frontend-(GUI)">Frontend (GUI)</a></li>
    <li><a href="#¿Cómo-se-construye-el-índice-invertido-en-PostgreSQL?">¿Cómo se construye el índice invertido en PostgreSQL?</a></li>
    <li><a href="#Experimentación">Experimentación</a></li>
    <li><a href="#conclusiones">Conclusiones</a></li>
    <li><a href="#referencias-bibliográficas">Referencias bibliográficas</a></li>
</details>

<hr>

# Introducción

## Objetivo del proyecto
El presente proyecto tiene como objetivo desarrollar estas estructuras de datos de manera eficiente, con motivo de realizar búsquedas rápidas en un conjunto de documentos.
Con respecto al índice invertido textual, se utiliza para asociar términos de consulta con los documentos que los contienen ya que mejora la velocidad y precisión del retorno de información, lo que facilita la recuperación eficiente de documentos relevantes en función de los términos de búsqueda.
En cuanto al índice multidimensional, se utilizar para representar características tanto de texto como de audio, lo que permite realizar consultas que involucren múltiples dimensiones, como la similitud de texto y audio en función de diferentes atributos.

## Dominio de datos
La base de datos utilizada es la Audio features and lyrics of Spotify songs, con al rededor de 18000 canciones con los campos:

|    **Campo**    |
|:---------------:|
| ```track_id```        | 
| ```track_name```  | 
| ```track_artist``` | 
| ```lyrics``` | 
| ```track_popularity``` | 
| ```track_album_id``` |
| ```track_album_name``` | 
| ```track_album_release_date``` |
| ```playlist_name``` |
| ```playlist_id``` |
| ```playlist_genre``` |
| ```playlist_subgenre``` |
| ```danceability``` |
| ```enery``` | 
| ```key``` | 
| ```loudness``` | 
| ```mode``` | 
| ```speechness``` | 
| ```acousticness``` | 
| ```instrumentalness``` | 
| ```liveness``` |
| ```valence``` |
| ```tempo``` |
| ```duration_ms``` |
| ```language``` |

## Importancia de aplicar indexación
La indexación es fundamental por las siguientes razones:
1. Recuperación eficiente de información: La indexación permite realizar búsquedas rápidas en grandes conjuntos de datos, lo que es esencial para la recuperación eficiente de documentos relevantes en función de consultas de texto y audio.

2. Optimización de consultas: Al indexar los datos, se pueden optimizar las consultas para que se ejecuten de manera más eficiente, lo que es crucial para aplicaciones en tiempo real, como la recuperación de información en sistemas de búsqueda.

3. Reducción de la complejidad computacional: La indexación puede reducir la complejidad computacional de las operaciones de búsqueda y análisis de datos, lo que es importante para garantizar un rendimiento óptimo del sistema, especialmente en aplicaciones que manejan grandes volúmenes de información.

# Estructura del proyecto
El algoritmo SPIMI (Single-Pass In-Memory Indexing) es un método utilizado para construir un índice invertido durante el proceso de indexación de grandes conjuntos de datos. A diferencia de algunos algoritmos de indexación que requieren múltiples pasadas sobre los datos, SPIMI realiza la construcción del índice en una sola pasada a través de los datos.

![spimi1](https://github.com/marceloZS/Full-Text-Search_Project2/blob/main/imagenes/spimi1.jpg)

Se calcula una sola vez la longitud de cada documento, y se lee el documento de entrada uno a uno (por ejemplo, un documento de texto) y se tokeniza en términos individuales. Cada término se procesa por separado.

![spimi2](https://github.com/marceloZS/Full-Text-Search_Project2/blob/main/imagenes/spimi2.jpeg)


# Backend (Índice Invertido)
El archivo inverted_index.py contiene la implementación del índice invertido utilizando el algoritmo SPIMI (Single-Pass In-Memory Indexing). El algoritmo SPIMI divide el proceso de indexación en bloques más pequeños para manejar grandes volúmenes de datos de manera eficiente.

## Construcción del índice invertido en memoria secundaria

```python

def spimi_invert(self):
    docs, total_terms = self.process_all()
    block_number = 0
    terms_processed = 0
    total_blocks = self.calcular_bloques(total_terms)
    terms_processed_per_block = math.ceil(total_terms/total_blocks)
    local_index = {}
    
    for i in docs:
        doc = i
        for term in doc["terms"]:
            if term not in local_index:
                local_index[term] = [{"id": doc["id"], "tf": 1}]
            else:
                # Comprueba si el id del documento ya existe para este término
                doc_found = False
                for doc_i in local_index[term]:
                    if doc_i["id"] == doc["id"]:
                        doc_i["tf"] += 1
                        doc_found = True
                        break
                if not doc_found:
                    # Si el id del documento no se encuentra después de la iteración completa, agrega un nuevo documento
                    local_index[term].append({"id": doc["id"], "tf": 1})
            terms_processed += 1
            if(terms_processed >= terms_processed_per_block):
                sorted_dictionary = collections.OrderedDict(sorted(local_index.items()))
                os.makedirs('local_indexes', exist_ok=True)
                with open(f'local_indexes/block_{block_number}.json', 'w') as file:
                    json.dump(sorted_dictionary, file)
                local_index.clear()
                block_number += 1
                terms_processed = 0

    # Comprueba si quedan términos en el último bloque
    if local_index:
        sorted_dictionary = collections.OrderedDict(sorted(local_index.items()))
        os.makedirs('local_indexes', exist_ok=True)
        with open(f'local_indexes/block_{block_number}.json', 'w') as file:
            json.dump(sorted_dictionary, file)
    self.binary_merge(total_blocks)

```

Iremos por partes:

```python
def spimi_invert(self):
    docs, total_terms = self.process_all()
    block_number = 0
    terms_processed = 0
    total_blocks = self.calcular_bloques(total_terms)
    terms_processed_per_block = math.ceil(total_terms/total_blocks)
    local_index = {}
```

- `process_all()`
    
    ```python
    def process_all(self):
        docs = []
        total_terms = 0
        for index, row in data.iterrows():
            doc = self.preprocess(row)
            total_terms += len(doc["terms"]) #Se toman en cuenta los terminos incluso esten repetidos, ya que en el merge en el peor de los casos ninguno de los terminos se repite, por lo que el tamaño de cada bloque debería ser lo suficientemente grande para que quepan 2^n terminos 
            docs.append(doc)
        return docs, total_terms
    ```
    
    - Itera cada uno de los documentos (rows) de nuestro csv (data textual)
        - Las preprocesa:
            - La tokeniza
            - Elimina las stepwords
            - Realiza Stemming
            - Finalmente el output sería una lista con cada una de las palabras ya preprocesadas
        - Agregamos en una variable la cantidad de términos en el documento.
        - Finalmente agregamos nuestro documento a la lista de documentos.
- `calcular_bloques(total_terms)`
    
    ```python
    def calcular_bloques(self, total_terms):
            total_bloques = total_terms // self.block_limit
            bloques_potencia_de_dos = 1
            while bloques_potencia_de_dos * 2 <= total_bloques:
                bloques_potencia_de_dos *= 2
            return bloques_potencia_de_dos
    ```
    
    El parámetro `total_terms` representa el número total de términos. La función divide este número por el límite de bloques (`self.block_limit`) para determinar cuántos bloques se pueden crear. Luego, utiliza un bucle while para encontrar la potencia de dos más grande que sea menor o igual al número de bloques calculado anteriormente.
    
    Finalmente, la función devuelve el número de bloques que se pueden crear, que es la potencia de dos encontrada en el bucle while.
    

```python
	for i in docs:
	    doc = i
	    for term in doc["terms"]:
		if term not in local_index:
		    local_index[term] = [{"id": doc["id"], "tf": 1}]
		else:
		    # Comprueba si el id del documento ya existe para este término
		    doc_found = False
		    for doc_i in local_index[term]:
			if doc_i["id"] == doc["id"]:
			    doc_i["tf"] += 1
			    doc_found = True
			    break
		    if not doc_found:
			# Si el id del documento no se encuentra después de la iteración completa, agrega un nuevo documento
			local_index[term].append({"id": doc["id"], "tf": 1})
		terms_processed += 1
```

Construimos un índice invertido en RAM llamado `local_index` a partir de una lista de documentos. El índice almacena los términos presentes en los documentos y para cada término, mantiene una lista de documentos asociados con su respectivo contador de frecuencia. Si un término ya está presente en el índice, se actualiza el contador de frecuencia para el documento correspondiente. Si el término no está presente, se agrega una nueva entrada en el índice con el documento y su contador de frecuencia inicializado en 1.

```python
	#Dentro del for term in doc["terms"]:
		if(terms_processed >= terms_processed_per_block):
		    sorted_dictionary = collections.OrderedDict(sorted(local_index.items()))
		    os.makedirs('local_indexes', exist_ok=True)
		    with open(f'local_indexes/block_{block_number}.json', 'w') as file:
			json.dump(sorted_dictionary, file)
		    local_index.clear()
		    block_number += 1
		    terms_processed = 0
```

Esta parte del código se encarga de guardar los índices locales en archivos separados (Bloques) cuando se alcanza un cierto número de términos procesados. Esto ayuda a dividir el proceso de indexación en bloques más pequeños y facilita la gestión de los datos, permitiendo que la RAM no llegue a su capacidad máxima al almacenar el índice invertido local.

```python
#Fuera de for i in docs:
    if local_index:
        sorted_dictionary = collections.OrderedDict(sorted(local_index.items()))
        os.makedirs('local_indexes', exist_ok=True)
        with open(f'local_indexes/block_{block_number}.json', 'w') as file:
            json.dump(sorted_dictionary, file)
    self.binary_merge(total_blocks)
```

Verifica si el diccionario `local_index` no está vacío. Si no lo está, ordena el diccionario, crea un directorio si no existe, y guarda el diccionario ordenado en un archivo JSON (Bloque).

Finalmente, ya que tenemos todos nuestros bloque llamamos a `binary_merge(total_blocks)`, que será explicado a continuación:

```python
def binary_merge(self, n_blocks):
    total_blocks = n_blocks
    merge_size = 1
    step = 0
    while merge_size < total_blocks:
        curr_block = 0
        while curr_block < total_blocks:
            next_block = curr_block + merge_size
            if next_block >= total_blocks:
                next_block = curr_block
                curr_block -= merge_size

            folder_name = 'local_indexes' if step == 0 else f'Pasada_{step}'
            with open(f'{folder_name}/block_{curr_block}.json', 'r') as file1:
                index1 = json.load(file1)
            with open(f'{folder_name}/block_{next_block}.json', 'r') as file2:
                index2 = json.load(file2)

            for key, value in index2.items():
                if key in index1:
                    index1[key].extend(value)
                else:
                    index1[key] = value

            merged_dict = index1

            os.makedirs(f'Pasada_{step+1}', exist_ok=True)
            with open(f'Pasada_{step+1}/block_{curr_block}.json', 'w') as file:
                json.dump(merged_dict, file)

            curr_block += merge_size * 2

        if step > 0:
            shutil.rmtree(f'Pasada_{step}')

        merge_size *= 2
        step += 1

    if step > 0:
        with open(f'Pasada_{step}/block_0.json', 'r') as file:
            global_index = json.load(file)
        keys = sorted(global_index.keys())
        block_size = len(keys) // n_blocks
        for i in range(n_blocks):
            if i == n_blocks - 1:
                block_keys = keys[i*block_size:]
            else:
                block_keys = keys[i*block_size:(i+1)*block_size]
            block_dict = {key: global_index[key] for key in block_keys}
            os.makedirs('global_index', exist_ok=True)
            with open(f'global_index/block_{i}.json', 'w') as file:
                json.dump(block_dict, file)

        shutil.rmtree(f'Pasada_{step}')
```

1. Inicialización de Variables:
    - **`total_blocks`**: Representa el número total de bloques que se fusionarán.
    - **`merge_size`**: Representa el tamaño de la fusión actual.
    - **`step`**: Representa la etapa actual del proceso de fusión.
2. Bucle Principal:
    - La fusión se realiza en varios niveles (etapas). En cada nivel, los bloques se fusionan en pares hasta que se obtiene un solo bloque.
    - En cada nivel, se duplica el tamaño de la fusión (**`merge_size *= 2`**).
    - En cada nivel, se realiza un bucle para fusionar los bloques actuales (**`curr_block`**) y los bloques adyacentes (**`next_block`**).
3. Fusión de Bloques:
    - Se abren los archivos JSON correspondientes a los bloques actuales y siguientes.
    - Se cargan los índices invertidos de los bloques en las variables **`index1`** e **`index2`**.
    - Se fusionan los índices combinando las listas de posteo para las mismas claves.
    - El resultado de la fusión se guarda en **`merged_dict`**.
4. Almacenamiento del Resultado de Fusión:
    - Se crea un nuevo directorio (**`Pasada_{step+1}`**) para almacenar los resultados de la fusión actual.
    - Se guarda el índice fusionado en un archivo JSON correspondiente al bloque actual.
5. Actualización de Variables:
    - Se actualiza **`curr_block`** para apuntar al siguiente par de bloques a fusionar.
    - El proceso se repite hasta que se han fusionado todos los bloques en un solo bloque.
6. Limpieza de Archivos Temporales:
    - Después de cada nivel de fusión, se elimina el directorio de la etapa anterior para liberar espacio.
7. Generación del Índice Global:
    - Después de la última fusión, se crea el índice global combinando los bloques resultantes en un solo índice invertido.
8. Almacenamiento del Índice Global:
    - El índice global se almacena en archivos JSON separados para cada bloque en el directorio **`global_index`**.
9. Limpieza Final:
    - Se eliminan los archivos temporales y directorios intermedios.

## Ejecución óptima de consultas aplicando Similitud de Coseno

La similitud de coseno es una medida de similitud entre dos vectores en un espacio multidimensional, utilizandose en la recuperación de información para comparar la similitud entre documentos o términos.

```python
def dict_query(self, query):
    query= self.process_query(query)
    query_tf = {term: query.count(term) for term in query}
    return query_tf
```

- La función **`process_query`** (que no está proporcionada en el código) se utiliza para preprocesar la consulta.
- La consulta se convierte en un diccionario donde las claves son los términos y los valores son las frecuencias de cada término en la consulta.

```python
def cosine_similarity(self, query_vector, doc_vectors, k):
    similarities = {}
    for doc_id, doc_vector in doc_vectors.items():
        doc_norm = np.linalg.norm(doc_vector)
        if doc_norm == 0:
            similarity =0
        else:
            similarity = np.dot(query_vector, doc_vector) / (np.linalg.norm(query_vector) * doc_norm)

        similarities[doc_id] = similarity
    # Ordenar los documentos por similitud
    sorted_docs = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
    # Seleccionar los k documentos más similares
    top_k_docs = [{'id': doc_id, 'score': score} for doc_id, score in sorted_docs[:k]]
    return top_k_docs
```

- Calcula la similitud coseno entre el vector de consulta y cada vector de documento.
- Los resultados se almacenan en un diccionario **`similarities`**, que se ordena según las puntuaciones de similitud en orden descendente.
- Se seleccionan los primeros k documentos más similares y se devuelven en un formato específico.

```python
# Construir vectores de documentos y vector de consulta
def build_document_vectors(self, query):
    # Inicializar variables
    terms = list(set())
    files = os.listdir('global_index')
    doc_vectors = {}  # Nuevo diccionario para almacenar los vectores de los documentos
    
    # Iterar sobre archivos de índice invertido para construir términos únicos
    for file in files:
        with open(os.path.join('global_index', file), 'r') as f:
            inverted_index = json.load(f)
            
            # Actualizar términos con los del índice invertido
            if inverted_index:
                if isinstance(inverted_index, list):
                    terms.update([item['term'] for w in inverted_index for item in w])
                else:
                    terms.update(inverted_index.keys())
    
    # Preparar lista de términos única y crear índice de términos
    terms = list(terms)
    terms.extend(query.keys())
    terms = sorted(set(terms))
    term_index = {term: index for index, term in enumerate(terms)}
    
    # Iterar sobre archivos de índice invertido para construir vectores de documentos
    for file in files:
        with open(os.path.join('global_index', file), 'r') as f:
            inverted_index = json.load(f)
            
            # Iterar sobre términos y documentos en el índice invertido
            for term, term_docs in inverted_index.items():
                # Definir 'term' para este contexto
                
                # Iterar sobre la información de documentos para el término
                for doc_info in term_docs:
                    doc_id = doc_info['id']
                    
                    # Inicializar el vector del documento si no existe
                    if doc_id not in doc_vectors:
                        doc_vectors[doc_id] = np.zeros(len(terms))
                    
                    # Actualizar el vector del documento con la frecuencia del término
                    tf = doc_info['tf']
                    doc_vectors[doc_id][term_index[term]] = tf
    
    # Actualizar los vectores de los documentos para que tengan la misma longitud que los términos
    for doc_id, vector in doc_vectors.items():
        if len(vector) < len(terms):
            doc_vectors[doc_id] = np.pad(vector, (0, len(terms) - len(vector)))
    
    # Inicializar vector de consulta con ceros y actualizar con frecuencias de términos en la consulta
    query_vector = np.zeros(len(terms))
    for term, tf in query.items():
        if term in inverted_index:
            df_t = len(inverted_index[term])
            if df_t == 0:
                df_t = 1
            idf_t = math.log(len(inverted_index) / df_t)
        
        if term in term_index:
            query_vector[term_index[term]] = tf
    
    return doc_vectors, query_vector

```

- `build_document_vectors()` construye vectores de documentos y un vector de consulta basados en un índice invertido. Se procesan los términos únicos y se construye un índice de términos. Luego, se iteran sobre los archivos de índice invertido para actualizar los vectores de documentos con las frecuencias de términos. Finalmente, se asegura de que los vectores de documentos tengan la misma longitud que la lista de términos y se construye el vector de consulta con las frecuencias de términos presentes en la consulta.

```python
def show_top_k(self, query, k, dataset):
    doc_vectors, query_vector = self.build_document_vectors(query)
    top_k_docs = self.cosine_similarity(query_vector, doc_vectors, k)
    for i, doc in enumerate(top_k_docs, 1):
        doc_id = doc['id']
        score = doc['score']
        doc_data = dataset[dataset['track_id'] == doc_id]
        print(f"Top {i} Document:")
        print(doc_data)
        print(f"Score: {score}\n")
```

- Utiliza las funciones anteriores para obtener los k documentos más similares a la consulta.
- Imprime información sobre estos documentos, incluidos los datos del conjunto de datos y las puntuaciones de similitud.

## ¿Cómo se construye el índice invertido en PostgreSQL?

A grandes rasgos, para la construcción del índice invertido en PostgreSQL se necesitan 3 tablas principales.
- Una tabla para almacenar los documentos
- Una tabla para almacenar los términos
- Una tabla de relación entre términos y documentos

A partir de esto, se requere extraer los términos de los documentos y almacenarlos en una tabla de términos. Por ejemplo, se tiene lo siguiente:
```sql
INSERT INTO terms (term)
SELECT DISTINCT unnest(string_to_array(lower(content), ' ')) AS term
FROM documents;
```

La función string_to_array se utiliza para dividir el contenido de los documentos en términos individuales, y la función unnest se utiliza para convertir el resultado en filas individuales.

Lo siguiente es armar la relación entre los documentos y términos. Esto se puede lograr utilizando consultas SQL que identifiquen los términos que aparecen en cada documento y los almacenen en la tabla de relación. Por ejemplo:
```sql
INSERT INTO document_term (document_id, term)
SELECT d.id, t.term
FROM documents d
JOIN terms t ON lower(d.content) LIKE '%' || t.term || '%';
```
Una vez que se han extraído los términos y se ha creado la tabla de relación, se pueden crear índices en las columnas relevantes para mejorar el rendimiento de las consultas de búsqueda. Por lo general, se crean índices en las columnas de términos y en las columnas de identificadores de documentos para acelerar las búsquedas.

Con el índice invertido ya construído se pueden realizar consultas de búsqueda utilizando cláusulas SQL como WHERE y JOIN. Estas consultas aprovechan los índices para buscar rápidamente los documentos que contienen los términos de búsqueda especificados. Por tal motivo, las búsquedas de texto se vuelven más eficientes, ya que se evita la necesidad de realizar exploraciones completas de los documentos.


# Backend (Índice Multidimensional)
- Extracción de características: 
Los vectores de características se almacenan en una base de datos PostgreSQL. Donde se realiza una consulta a la tabla `vectores` de la base de datos, y los resultados se almacenan en el diccionario `features`, donde las claves son los identificadores de las pistas (track_id) y los valores son los vectores de características (mfcc).

- Código para extraer características:

```python
query = feature_extraction("/Directory")
query_vector = query

```

## KNN Secuencial: (Sin indexación)
El algoritmo KNN-secuencial es una implementación básica y directa del algoritmo de los k-vecinos más cercanos (KNN) que realiza una búsqueda exhaustiva de los vecinos más cercanos sin utilizar estructuras de datos especializadas para acelerar las consultas, sólo utilizando una cola de prioridad básica.

Para la búsqueda KNN-secuencial, no se implementó ninguna técnica con indexación por lo que no mejora la eficiencia en las búsquedas. El algoritmo evalúa los puntos de datos en el conjunto para encontrar los `k` vecinos más cercanos al punto de la consulta. En está técnica calculamos la similitud que al ser sin indexación conlleva una gran complejidad computacional. 
Se implementó los siguientes algoritmos: `KnnSearch(Q, k)`, `RangeSearch(Q, r)` 

![knn_search](https://github.com/Diegospf12/CapibaraGrooveFinder/assets/91237434/f534b6b0-7b1b-4c5f-8f66-5d3ff1f27874)
.png)

- `KnnSearch(Q, k)`: Recibe el vector de consulta 'query_vector' y un entero 'k' que representa la cantidad de vecinos más cercanos a buscar. Se realiza la consutla a la base de datos para obtener los vectores característicos de audio, luego calculamos la distancia euclidiana entre el vector de consulta y todos los vectores en la base de datos. Utilizamos `heapq' para encontrar los 'k' elementos más pequeños. Al final devuelve la lista de tuplas, con el identificador de audio y la distancia euclidiana. 

![KNN_RANGE](https://github.com/Diegospf12/CapibaraGrooveFinder/assets/91237434/82ba852a-d2fb-4364-bced-6f10e3276f17)



- `Range_Search`: Al igual que el KnnSearch, recibe el vector de consulta 'query_vector' pero con el valor del radio 'radius'. Se realiza la búsqueda en la base de datos para obtener los vectores caracteristicos, se selecciona de la tabla 'songs'. Realiza el cálculo de la distancia euclidiana, filtra las distancias para incluir solo aquellos vectores que estan en el radio de búsqueda. Al final devuelve una lista de tuplas que contiene la distancia euclidiana y el 'track'.

## KNN RTree

Para que la búsqueda sea más eficiente, hacemos uso del `RTree` como una libreria de índice espacial para indexar todos los vectores característicos. La búsqueda RTree en el KNN donde el rango es inicialmente infinito, luego se va reduciendo el rango según se van evaluando. 

![R-Tree](https://github.com/Diegospf12/CapibaraGrooveFinder/assets/91237434/a00a2664-b629-42ff-8a65-4f875f457963)


- `KNN RTree`: 

Ejecutamos una consulta SQL para obtener los identificadores de las pistas 'track_id' y sus vectroes caracteríticos 'mffcc' desde la tabla 'vectores'. Las caracteríticas se almancenan en el dict 'features'. Para la construcción del índice R-tree, utilizamos el módulo rtree para crear el índice, lo configuramos con la propiedad de 'p.dimension'. Se insertan los objetos en el índice RTree utlizandos los identificadores de las pistas y los vectores caracteríticos concatenados.
La función `knn_search_rtree` va a recibir un vector de consulta 'query_vector' y un entro 'k' que representa la cantdiad de vecinos más cercanos. Calculamos la distancia euclidiana entre el vector de consulta y los objetos encontrados en el índice. Al final devolvemos una lista de tuplas, donde cada tupla contiene el identificador del audio y la distancia euclidiana correspondiente. 


## KNN HighD

El algoritmo KNN en espacios de alta dimensión (High D) es un método de aprendizaje supervisado que se utiliza para clasificación y regresión. Dado un conjunto de datos de entrenamiento con etiquetas conocidas, el algoritmo KNN clasifica nuevos ejemplos en función de la similitud de sus características con las de los ejemplos de entrenamiento.


### **¿Qué la maldición de la dimensionalidad?**

La efectividad del algoritmo KNN disminuye en entornos de alta dimensionalidad debido a desafíos específicos. 

En un espacio de alta dimensión, la eficiencia del algoritmo KNN puede verse afectada debido a la "maldición de la dimensionalidad". Esto se refiere al fenómeno en el que el volumen del espacio de características aumenta tan rápidamente con el aumento de la dimensionalidad que los datos se vuelven escasos y dispersos. A medida que se incrementa el número de características, los cálculos de distancias y la identificación de vecinos cercanos se vuelven más costosos computacionalmente. La premisa de que puntos similares están cercanos se vuelve menos válida, ya que las distancias entre puntos pierden su distintividad. 

Para superar este problema, se utilizan técnicas de reducción de la dimensionalidad o usos de métodos de indexación eficientes. En nuestro caso, aplicamos el FAISS de Facebook para acelerar las consultas.

![Análisis1](https://github.com/Diegospf12/CapibaraGrooveFinder/assets/91237434/2afb3f3c-4994-4c3b-98ee-15298d10da33)

## Análisis de la maldición de la dimensionalidad y como mitigarlo

![Análisis](https://github.com/Diegospf12/CapibaraGrooveFinder/assets/91237434/22053932-3678-4d87-aa29-186f2a643ef0)


### **¿Cómo mitigarlo?**

**`Reducción de Datos: `**

Aborda la maldición de la dimensionalidad utilizando técnicas como selección y extracción de funciones (PCA, kernel) para conservar la relevancia en espacios de baja dimensión.

**`K-NN Aproximado`**

Cuando la búsqueda exacta se vuelve costosa, se opta por algoritmos de k-NN aproximado. El hash sensible a la localidad (LSH) divide elementos similares en depósitos de alta probabilidad, ofreciendo una solución rápida para k-NN en entornos de alta dimensión. Proyecciones aleatorias y bosques de proyección aleatoria (rpForests) permiten transformar datos y realizar agrupaciones aproximadas de manera eficiente para encontrar vecinos más cercanos.

### Faiss (Facebook AI Similarity Search) 

Es conocida por su eficacia en la búsqueda de vecinos más cercanos y la búsqueda de similitud en espacios vectoriales. En este caso utlizaremos el índice de Faiss **`IndexIVFFlat`** que utilza una técnica llamada Inverted File Indexing (IVF) y utiliza el cuantizador plano **`IndexFlatL2`** para cuantificar los vectores en las celdas del índice IVF.


![faiss](https://github.com/Diegospf12/CapibaraGrooveFinder/assets/91237434/0a87f89b-3335-48fe-90e2-d24b2b5a7783)

![ejem](https://github.com/Diegospf12/CapibaraGrooveFinder/assets/91237434/f722da10-0132-4b48-bb34-51c8395cb865)


**Creación del índice Faiss:**

```python
quantizer = faiss.IndexFlatL2(feature_matrix.shape[1])
index = faiss.IndexIVFFlat(quantizer, feature_matrix.shape[1], 3)
```
- Se utiliza **`faiss.IndexIVFFlat`** como índice Inverted File Index (IVF) plano. Este índice segmenta el espacio de búsqueda en celdas, organizando una lista invertida para cada celda. La construcción de listas invertidas facilita la búsqueda eficiente en conjuntos de datos de alta dimensionalidad, ya que reduce el espacio de búsqueda a celdas específicas, mejorando significativamente la velocidad de recuperación de vecinos más cercanos. Difinimos a 'nprobe' (Cuantos `centroides` se exploran durante la búsuqeda) con 3 pero se puede mejorar según la presición de la búsqueda y la velocidad.  

- Se utiliza **`faiss.IndexFlatL2`** como cuantizador plano. Este componente se encarga de asignar los vectores de características a celdas específicas en función de su proximidad, utilizando la distancia euclidiana como medida de proximidad. Esta elección de cuantizador permite una rápida cuantificación de los vectores para su posterior indexación.


**Adición de datos al índice:**

```python
index.train(feature_matrix)
index.add(feature_matrix)
```
Se entrena el `índice Faiss` con la matriz de características utilizando el método 'train'. Luego se añaden los vectores de características al índice utilizando el método 'add'.

**Lectura y escritura del índice:**

```python
faiss.write_index(index, 'index_file')
```
- Utilizando el método write_index.

**La búsqueda de vecinos más cercanos:**
```python
distances, indices = index.search(query_matrix, K)
```
- Se realiza una búsqueda de k vecinos más cercanos en el índice Faiss utilizando el vector de consulta 'query_vector'. Devuelve una lista de tuplas, donde cada tupla contiene el identificador de la pista de audio (audio_path) y la distancia asociada.
  
![index2](https://github.com/Diegospf12/CapibaraGrooveFinder/assets/91237434/05d19b20-dca9-4079-8613-77c525fc7b5c)

![index](https://github.com/Diegospf12/CapibaraGrooveFinder/assets/91237434/e7be27f1-a093-45ec-a533-122459d36f6e)

- **Desventajas**
    -  Consumo de memoria: La creación de índices IVF puede requerir más memoria, siendo una limitación en conjuntos de datos grandes o en entornos con recursos limitados.
    - Entrenamiento: Antes de las búsquedas, el índice IVF necesita ser entrenado con datos de entrenamiento, añadiendo un paso computacionalmente costosos, especialmente para conjuntos de datos extensos.
    - Tamaño del índice: Los índices IVF tienden a ser más grandes en comparación con índices más simples, lo que puede ser crítico si el espacio de almacenamiento es limitado.



`Fuentes:`
- https://www.baeldung.com/cs/k-nearest-neighbors
- https://es.quora.com/Qu%C3%A9-es-la-maldici%C3%B3n-de-la-dimensionalidad
- https://www.youtube.com/watch?v=nhgCwWGNDiM


# Frontend (GUI)

## Mini-manual de usuarios
### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/Diegospf12/CapibaraGrooveFinder
cd CapibaraGrooveFinder
```

### Paso 2: Configuración del Backend

Instalar dependencias
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

Ejecutar servidor
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Paso 3: Configuración del Frontend

Instalar dependencias
```bash
cd frontend
npm install
npm run serve
```

## Screenshots
![[Main page]](https://github.com/Diegospf12/CapibaraGrooveFinder/blob/main/images/main.png)
![[Lyrics page]](https://github.com/Diegospf12/CapibaraGrooveFinder/blob/main/images/lyrics.png)
![[Similar page]](https://github.com/Diegospf12/CapibaraGrooveFinder/blob/main/images/similarpage.png)

## Análisis comparativo visual con otras implementaciones
![[Similar page]](https://github.com/Diegospf12/CapibaraGrooveFinder/blob/main/images/example1.png)
![[Similar page]](https://github.com/Diegospf12/CapibaraGrooveFinder/blob/main/images/example2.png)

# Experimentación

## Tablas y gráficos de los resultados experimentales

|      | Implementación | Postgress |
|------|----------------|-----------|
| 1000 |     15 ms      |   19 ms   |
| 2000 |     34 ms      |   33 ms   |
| 4000 |     65 ms      |   72 ms   |
| 8000 |    190 ms      |  180 ms   |
|16000 |    295 ms      |  300 ms   |
|32000 |    333 ms      |  359 ms   |
|64000 |    380 ms      |  360 ms   |


### Implementación de Índice Invertido

Nuestra implementación personalizada de índice invertido ha demostrado ser eficiente en la búsqueda de datos basada en texto. Hemos medido el rendimiento de nuestra implementación en milisegundos para una variedad de tamaños de datos de prueba, desde 1,000 hasta 64,000 registros. 

### PostgreSQL con Índice Invertido

Por otro lado, hemos utilizado PostgreSQL con sus propios índices invertidos para realizar búsquedas de texto similares a nuestras pruebas con datos de prueba de tamaños comparables.

### Gráfico comparativo

![graph1](https://github.com/Diegospf12/CapibaraGrooveFinder/blob/main/images/grafico_comparativo_1.png)

## Tabla de resultados de índices multidimensionales

Ejecutamos el KNN-RTree, KNN-secuencial y el KNN-HighD sobre una colección de objetos de tamaño N y comparamos la eficiencia en función del tiempo de ejecución

|  k=8 | Secuencial |  KNN-RTree  |  KNN-HighD  |
|------|------------|-------------|-------------|
| 1000 | 0.02148 ms | 0.001276 ms | 0.011387 ms |
| 2000 | 0.03314 ms | 0.002307 ms | 0.013839 ms |
| 4000 | 0.04983 ms | 0.006453 ms | 0.013992 ms |
| 8000 | 0.09919 ms | 0.015350 ms | 0.015020 ms |
|12000 | 0.16726 ms | 0.026420 ms | 0.015874 ms |
|16000 | 0.17850 ms | 0.035708 ms | 0.015996 ms |

### Gráfico comparativo de tiempos

![graph2](https://github.com/Diegospf12/CapibaraGrooveFinder/blob/main/images/grafico_comparativo_2.png)


### Análisis y Discusión
- Se puede ver que el índice IVFFlat de Faiss es el método más óptimo para la búsqueda por similitud ya que es el que mejor se mantiene mientras más vectores aparecen en la colección.

- La búsqueda KNN con Rtree empieza siendo la mejor cuando hay pocos vectores, pero a medida que la cantidad de vectores van incrementando, se va haciendo más ineficiente.

- La búsqueda secuencial es la menos eficiente de todas, se puede notar que su crecimiento a medida que van apareciendo más vectores es exponencial.

- Nuestra implementación de índice invertido a la hora de hacer el filtrado pierda algunos términos ya que estos pueden estar concatenados con símbolos raros (".!-) y esto puede ocacionar que la búsqueda de ciertos documentos que contienen estas palabras no sean exactos.

### Conclusiones

Los resultados de nuestra comparación indican que PostgreSQL supera ligeramente a nuestra implementación personalizada de índice invertido en términos de rendimiento en la mayoría de los escenarios. Aunque nuestra implementación es eficiente, PostgreSQL, con su optimización interna y capacidad para manejar grandes conjuntos de datos, muestra tiempos de búsqueda ligeramente más bajos en las pruebas. Por otro lado a la hora de búsqueda por similitud de audio, podemos darnos cuenta que la mejor opción fue el Índice IVFFlat de Faiss ya que esye divide los audios por clústers, para asi reducir la cantidad de comparaciones.


### Referencias bibliográficas



- A. Guttman. R-trees: A dynamic index structure for spatial searching. In Proc. ACM International Conference on Management of Data (SIGMOD’84), pages 47—57. ACM Press 1984
- Baeldung. (s.f.). K-Nearest Neighbors (KNN) Algorithm in C#. Baeldung. https://www.baeldung.com/cs/k-nearest-neighbors
- Facebook Research. (Año). Faiss: A library for efficient similarity search and clustering. Recuperado de https://github.com/facebookresearch/faiss
- FAISS. (s.f.). IndexIVFFlat. Faiss. https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexIVFFlat.html
- Pinecone. Faiss Tutorial. Pinecone Learn. https://www.pinecone.io/learn/series/faiss/faiss-tutorial/

### Tareas asignadas

![tasks](https://github.com/Diegospf12/CapibaraGrooveFinder/blob/main/images/tasks.png)

