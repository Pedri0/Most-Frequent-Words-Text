# Most-Frequent-Words-Text

Programa de Python que permite encontrar las palabras más frecuentes en un texto.

Uso:
```bash
    $ python3 top_words_text.py --ngram_min=2 --ngram_max=3 --custom_stopwords="["eg", "etc", "usw", "also", "ever"]"
```
ngram_min: Número mínimo de n-gramas que se van a considerar en el análisis.
ngram_max: Número máximo de n-gramas que se van a considerar en el análisis.
custom_stopwords: Lista extra de palabras vacías que se van a considerar en el análisis.

Ejecutar el programa guarda un archivo .csv con los resultados del análisis y una imagen png con un gráfico de barras con los resultados.

Para las respuestas a las preguntas del ejercicio, ver el archivo [top_words_text.ipynb](top_words_text.ipynb). El archivo [top_words_text.py](top_words_text.py) se generó para realizar un código accionable.

## Requerimientos
Para instalar los requerimientos, ejecutar:

```bash
$ pip install -r requirements.txt
```