import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json

#Esta función recibe una URL y un nombre de archivo, y guarda el texto extraído de la URL en el archivo.	
def fetch_and_extract_text(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        #Este código elimina los scripts y estilos de la página.
        for element in soup(["script", "style"]):
          element.extract()
        extracted_text = soup.get_text()

        extracted_text = ' '.join(extracted_text.split())
        return extracted_text
    else:
        return f"Error: No puede obtenerse datos de: {url}"
    
#Función para cargar los documentos que estan en el json
def load_documents_from_json(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        documents = json.load(file)
    return documents

#Funcion para insertar documentos si no existen
def insert_documents_to_mongo(documents):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["websiteLists"]
    collection = db["websites"]

    if "websites" not in db.list_collection_names():
        db.create_collection("websites")

    for document in documents:
        if not collection.find_one({"url": document["url"]}):  # Evita insertar duplicados
            collection.insert_one(document)
            print(f"Documento insertado: {document['nombre']}")
        else:
            print(f"El documento ya existe: {document['nombre']}")
    
#Esta función obtiene las URLs de la base de datos de MongoDB.
def get_websites_from_mongo(): 
    client = MongoClient("mongodb://localhost:27017/")
    db = client["websiteLists"] #Mi base de datos
    collection = db["websites"] #Mi colección
    return list(collection.find())


# Guarda el texto extraído en la base de dato. 
def save_text_to_mongo(document_id, text):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["websiteLists"]
    collection = db["websites"]
    collection.update_one({"_id": document_id}, {"$set": {"text": text}})

#Función principal
if __name__ == "__main__":
    json_file = "data.json"
    documents = load_documents_from_json(json_file)

    insert_documents_to_mongo(documents)

    documents = get_websites_from_mongo()

    if not documents:
        print("No hay documentos en la base de datos.")
    else:
        for index, document in enumerate(documents):
            url = document["url"]
            print(f"Obteniendo el texto de: {url}")
            extracted_text = fetch_and_extract_text(url)

            filename = f"extracted_text_{index+1}.txt"
            with open(filename, "w", encoding="UTF-8") as file:
                file.write(extracted_text)

            print(f"Guardando el texto extraído en: {filename}")

            save_text_to_mongo(document["_id"], extracted_text)
            print(f"Guardando el texto extraído en MongoDB para el documento: {document["nombre"]}")



