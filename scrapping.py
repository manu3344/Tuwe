import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

#Esta función recibe una URL y un nombre de archivo, y guarda el texto extraído de la URL en el archivo.	
def fetch_and_extract_text(url, filename):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        #Este código elimina los scripts y estilos de la página.
        for element in soup(["script", "style"]):
          element.extract()
        extracted_text = soup.get_text()

        extracted_text = ' '.join(extracted_text.split())

        #Aqui se guarda el texto extraído en un archivo.
        with open(filename, "w", encoding="utf-8") as file:
            file.write(extracted_text)
        return extracted_text
    else:
        return f"Error: No puede obtenerse datos de: {url}"
    
#Esta función obtiene las URLs de la base de datos de MongoDB.
def get_websites_from_mongo(): 
    client = MongoClient("mongodb://localhost:27017/")
    db = client["websiteLists"] #Mi base de datos
    collection = db["websites"] #Mi colección

    urls = []
    for document in collection.find():
        urls.append(document["url"])
    return urls

if __name__ == "__main__":

    urls = get_websites_from_mongo()
    for index, url in enumerate(urls):
        print(f"Obteniendo el HTML de: {url}")
        filename = f"extracted_text_{index+1}.txt"
        extracted_text = fetch_and_extract_text(url, filename)
        print("Texto extraído:")
