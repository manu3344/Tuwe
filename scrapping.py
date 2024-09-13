import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

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
    
#Esta función obtiene las URLs de la base de datos de MongoDB.
def get_websites_from_mongo(): 
    client = MongoClient("mongodb://localhost:27017/")
    db = client["websiteLists"] #Mi base de datos
    collection = db["websites"] #Mi colección

    return list(collection.find())

def save_text_to_mongo(document_id, text):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["websiteLists"]
    collection = db["websites"]
    collection.update_one({"_id": document_id}, {"$set": {"text": text}})

if __name__ == "__main__":

    documents = get_websites_from_mongo()

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



