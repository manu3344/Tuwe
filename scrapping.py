import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

websitesLists = [
    "https://centralgps.com.mx/", 
    "https://www.lala.com.mx/", 
]

def fetch_and_extract_text(url, filename):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        for element in soup(["script", "style"]):
          element.extract()
        extracted_text = soup.get_text()

        extracted_text = ' '.join(extracted_text.split())
        with open(filename, "w", encoding="utf-8") as file:
            file.write(extracted_text)
        return extracted_text
    else:
        return f"Error: No puede obtenerse datos de: {url}"
    
def print_mongo_values(): 
    client = MongoClient("mongodb://localhost:27017/")
    db = client["websiteLists"]
    collection = db["websites"]
    for website in collection.find():
        print(website)

if __name__ == "__main__":
    for index, url in enumerate(websitesLists):
        print(f"Obteniendo el HTML de: {url}")
        filename = f"extracted_text_{index+1}.txt"
        extracted_text = fetch_and_extract_text(url, filename)
        print("Texto extraído:")

    print("Valores de la base de datos:")
    print_mongo_values()