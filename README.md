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
La base de datos utilizada es la Fashion Product Images. Esta contiene alrededor de 44 mil productos etiquetados por ID, categoría, género, color, año, etc.

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

El código incluye las siguientes funciones principales:

1. spimi_invert(): Esta función realiza la indexación de los documentos presentes en una carpeta de entrada. Utiliza el algoritmo SPIMI para generar el índice invertido.

2. binary_search_term_blocks(): Esta función realiza una búsqueda binaria en los bloques del índice invertido para encontrar un término específico. Utiliza una implementación eficiente de búsqueda binaria para mejorar el rendimiento de la búsqueda.

3. cosine_similarity(): Esta función calcula la similitud de coseno entre una consulta y los documentos indexados. Utiliza el índice invertido y los pesos TF-IDF para calcular la similitud de coseno.

## 1. MÉTODO SPIMI INVERT()

```python

def spimi_invert(self):
        documents = os.listdir(self.input_folder)
        documents_count = len(documents)
        documents_counter = 0
        block_number = 0

        for docID in documents:
            if docID.endswith(".txt"):
                documents_counter += 1
                file_route = os.path.join(self.input_folder, docID)
                file_content = open(file_route, encoding="utf-8").read().lower()

```

Leemos uno a uno de nuestros documentos no pre-procesados

```python
                '''Pre-processing'''
                # Tokenizamos nuestro txt
                tokens = nltk.word_tokenize(file_content)
                #Filtramos para que no pertenezca a los stopwords o no sea un valor no alfanumerico (Stopwords / Valores raros)
                terms = [word for word in tokens if not word in TextPreprocessor.stopwords and re.match("^[a-zA-Z]+$", word)]
                #Hacemos Stemming en el idioma respectivo
                terms = [TextPreprocessor.stemmer.stem(w) for w in terms]
```
Una vez obtenemos el documento no procesado:
- Lo tokenizamos
- Filtramos las Stopwords
- Hacemos Stemming

```python
                for term in terms:

                    if (sys.getsizeof(term) + sys.getsizeof([docID]) + sys.getsizeof(self.dictionary) > self.block_size_limit):
                        temp_dict = self.sort_terms()
                        self.write_block_to_disk(temp_dict, block_number)
                        temp_dict = {}
                        block_number += 1

                    if term not in self.dictionary:
                        self.dictionary[term] = [docID]
                    else:
                        self.dictionary[term].append(docID)

                if sys.getsizeof(self.dictionary) > self.block_size_limit or (documents_counter == documents_count - 1):
                    temp_dict = self.sort_terms()
                    self.write_block_to_disk(temp_dict, block_number)
                    temp_dict = {}
                    block_number += 1
```

Una vez ya pre-procesado el documento, leemos uno a uno los términos de este, y los vamos agregando al diccionario de la siguiente forma:

```python
diccionario = {'baron':['doc1278.txt', 'doc1299.txt'],
        'zascuss':['doc1278.txt'],
        'abbi': ['doc1299.txt'],
        'abraim' : ['doc12081.txt']
}
```

Una vez este diccionario llegue al límite de RAM:

- Ordenaremos este diccionario en orden alfabético (sort_terms(self))
- y agregaremos su term frequency de la siguiente forma (sort_terms(self) llama al método calculate_tftd(self, pl_with_duplicates)):

```python
diccionario_temporal = {    'aaron':[['doc11987.txt', 1]],
                            'abascuss':[['doc1278.txt', 1], ['doc1998.txt', 6]],
                            'abbi':[['doc1299.txt', 2]],
                            'abf':[['doc1156.txt', 3]],
                            'abraim':[['doc12081.txt', 1]]  }
```
- Finalmente, este diccionario modificado lo cargamos a memoria secundaria con el método write_block_to_disk(self, term_postings_list, block_number), generando así un bloque (indice invertido local).

**Una vez se hayan terminado de procesar todos los documentos, y con ello haber creado todos los bloques, mergearemos todos estos bloques para crear un indice invertido global repartido en los n bloques.**

```python
        print("BLOCKS creation complete!")
        self.merge_blocks()
```

```python
Insertar codigo de merge blocks


```
Explicar código de merge blocks



## Ejecución óptima de consultas aplicando similitud de coseno



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

## Tabla de resultados de índices multidimensionales

Ejecutamos el KNN-RTree, KNN-secuencial y el KNN-HighD sobre una colección de objetos de tamaño N y comparamos la eficiencia en función del tiempo de ejecución

|  k=8    | Secuencial |  KNN-RTree  |  KNN-HighD  |
|------|------------|-------------|-------------|
| 1000 | 0.05100 ms | 0.001276 ms | 0.053848 ms |
| 2000 | 0.08857 ms | 0.002307 ms | 0.087420 ms |
| 4000 | 0.16724 ms | 0.006453 ms | 0.155970 ms |
| 8000 | 0.28190 ms | 0.015350 ms | 0.256640 ms |
|12000 | 0.49926 ms | 0.026420 ms | 0.397190 ms |
|16000 | 0.63667 ms | 0.035708 ms | 0.486560 ms |

### Gráfico comparativo de tiempos

![graph2](https://github.com/Diegospf12/CapibaraGrooveFinder/blob/main/images/grafico_comparativo_2.png)


### Análisis y Discusión
- Podemos notar que el la búsqueda KNN con un RTree es la que menos tiempo demora, esto se debe a que a la hora de indexar los vectores, estos se transforman a un vector en 2D, por lo que a la hora de hacer una búsqueda el tiempo computacional será menor a comparación de la búsqueda secuencial y con el índice IVFFlat, los cualés hacen una búsqueda en 50D.

- El tiempo de la búsqueda secuencial va incrementando mucho a medida que se va incrementando la cantidad de vectores en la colección, por lo que podemos notar que a la hora de búsquedas en altas dimensiones, el índice IVFFlat será más óptimo.

- Nuestra implementación de índice invertido a la hora de hacer el filtrado pierda algunos términos ya que estos pueden estar concatenados con símbolos raros (".!-) y esto puede ocacionar que la búsqueda de ciertos documentos que contienen estas palabras no sean exactos.

### Conclusión

Los resultados de nuestra comparación indican que PostgreSQL supera ligeramente a nuestra implementación personalizada de índice invertido en términos de rendimiento en la mayoría de los escenarios. Aunque nuestra implementación es eficiente, PostgreSQL, con su optimización interna y capacidad para manejar grandes conjuntos de datos, muestra tiempos de búsqueda ligeramente más bajos en las pruebas. Por otro lado a la hora de búsqueda por similitud de audio, podemos darnos cuenta que la mejor opción fue el Índice IVFFlat de Faiss ya que esye divide los audios por clústers, para asi reducir la cantidad de comparaciones.
