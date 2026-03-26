import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import json

def extraer_palabras_de_epub(ruta_archivo):
    libro = epub.read_epub(ruta_archivo)
    palabras_libro = set()

    for item in libro.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            sopas = BeautifulSoup(item.get_content(), 'html.parser')
            texto = sopas.get_text()

            #quitar números y puntuación, convertir a minúsculas
            palabras = re.findall(r'\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+\b', texto.lower())
            palabras_libro.update(palabras)

    return palabras_libro

def ejecutar_proyecto(lista_epubs):
    set_global = set()

    for ruta in lista_epubs:
        print(f"Procesando: {ruta}...")
        try:
            palabras = extraer_palabras_de_epub(ruta)
            set_global.update(palabras)
        except Exception as e:
            print(f"Error con {ruta}: {e}")

    with open('vocabulario_extraido.json', 'w', encoding='utf-8') as f:
        json.dump(list(set_global), f, ensure_ascii=False, indent=4)

    print(f"Proceso terminado. Total de palabras únicas: {len(set_global)}")

mis_libros = ['libro1.epub', 'libro2.epub', 'libro3.epub']
ejecutar_proyecto(mis_libros)
