# Capibara Groove Finder
Proyecto 3 del curso de Base de datos 2. Construcción del índice invertido textual y multidimensional

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

## Índice invertido textual
El índice invertido es una estructura de datos utilizada en motores de búsqueda y sistemas de recuperación de información. Consiste en un diccionario que mapea términos a una lista de documentos en los que aparecen esos términos. Esta estructura permite una búsqueda eficiente de documentos que contengan ciertos términos clave. 

## Índice multidimensional
Un índice multidimensional es una estructura de datos que permite organizar y acceder a información en múltiples dimensiones. Se utiliza para representar y buscar datos que tienen múltiples atributos o características.

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
def build_document_vectors(self, query):
    terms = list(set())
    files = os.listdir('global_index')
    doc_vectors = {}  # Nuevo diccionario para almacenar los vectores de los documentos
    for file in files:
        with open(os.path.join('global_index', file), 'r') as f:
            inverted_index = json.load(f)
            if inverted_index:
                if inverted_index:
                    if isinstance( inverted_index, list):
                        terms.update([item['term'] for w in inverted_index for item in w])
                    else:
                        terms.update(inverted_index.keys())
    terms = list(terms)
    terms.extend(query.keys())
    terms = sorted(set(terms))
    term_index = {term: index for index, term in enumerate(terms)}
    for file in files:
        with open(os.path.join('global_index', file), 'r') as f:
            inverted_index = json.load(f)
            for term, term_docs in inverted_index.items():  # Definir 'term' aquí
                for doc_info in term_docs:
                    doc_id = doc_info['id']
                    if doc_id not in doc_vectors:
                        doc_vectors[doc_id] = np.zeros(len(terms))  # Inicializar el vector del documento
                    tf = doc_info['tf']
                    doc_vectors[doc_id][term_index[term]] = tf  # Actualizar el vector del documento
    # Actualizar los vectores de los documentos para que tengan la misma longitud que los términos
    for doc_id, vector in doc_vectors.items():
        if len(vector) < len(terms):
            doc_vectors[doc_id] = np.pad(vector, (0, len(terms) - len(vector)))
    query_vector = np.zeros(len(terms))
    for term, tf in query.items():
        if term in inverted_index:
            df_t = len(inverted_index[term])
            if idf_t == 0:
                df_t = 1
            idf_t = math.log(len(inverted_index) / df_t)
        if term in term_index:
            query_vector[term_index[term]] = tf
    return doc_vectors, query_vector
```

1. **Obtención de Términos Únicos:**
    - **`terms = list(set())`**: Se inicializa una lista vacía para almacenar términos únicos.
    - Se obtienen los archivos en el directorio 'global_index' que contienen los índices invertidos de los documentos.
    - Se recorre cada archivo y se carga el índice invertido de cada documento.
2. **Actualización de Términos con Índice Invertido:**
    - Se verifica si el índice invertido está presente y si es una lista.
    - Si es una lista, se agregan los términos a la lista **`terms`** extrayendo el término de cada elemento en la lista.
    - Si no es una lista, se asume que es un diccionario y se agregan las claves del diccionario a **`terms`**.
3. **Manejo de Términos de Consulta:**
    - Se agregan los términos presentes en la consulta (**`query.keys()`**) a la lista de términos (**`terms`**).
    - La lista de términos se ordena y se eliminan duplicados.
4. **Creación del Índice de Términos:**
    - Se crea un diccionario **`term_index`** donde las claves son los términos y los valores son los índices correspondientes en el vector.
5. **Construcción de Vectores de Documentos:**
    - Se recorren nuevamente los archivos de índice invertido.
    - Para cada término en el índice invertido y sus documentos asociados, se actualiza el vector del documento (**`doc_vectors`**) con la frecuencia del término (**`tf`**) en ese documento.
6. **Ajuste de Longitud de Vectores de Documentos:**
    - Después de construir los vectores para todos los documentos, se verifica si algún vector es más corto que la longitud total de términos.
    - Si es más corto, se agrega relleno (**`np.pad`**) para que todos los vectores tengan la misma longitud.
7. **Construcción del Vector de Consulta:**
    - Se inicializa un vector de ceros para la consulta (**`query_vector`**) con la misma longitud que la lista de términos.
    - Se actualiza el vector de consulta con las frecuencias de términos presentes en la consulta.
8. **Cálculo del IDF para la Consulta:**
    - Para cada término en la consulta, se calcula el Inverse Document Frequency (IDF) utilizando la fórmula **`idf_t = math.log(len(inverted_index) / df_t)`**, donde **`df_t`** es la frecuencia documental del término.
9. **Retorno de Resultados:**
    - La función devuelve dos objetos: **`doc_vectors`**, un diccionario donde las claves son los ID de documentos y los valores son los vectores de documentos; y **`query_vector`**, el vector de la consulta.

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



## KNN Secuencial: Priority Queue Search y Range Search



## KNN RTree



## KNN High D: Mitigación de la dimensionalidad con FAISS



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

### Conclusión

Los resultados de nuestra comparación indican que PostgreSQL supera ligeramente a nuestra implementación personalizada de índice invertido en términos de rendimiento en la mayoría de los escenarios. Aunque nuestra implementación es eficiente, PostgreSQL, con su optimización interna y capacidad para manejar grandes conjuntos de datos, muestra tiempos de búsqueda ligeramente más bajos en las pruebas. Por otro lado a la hora de búsqueda por similitud de audio, podemos darnos cuenta que la mejor opción fue el Índice IVFFlat de Faiss ya que esye divide los audios por clústers, para asi reducir la cantidad de comparaciones.





