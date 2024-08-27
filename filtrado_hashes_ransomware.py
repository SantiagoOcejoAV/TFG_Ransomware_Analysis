import requests
import csv
import time

#busqueda en malwarebazaar
def search_malware_bazaar(hashes):
    resulted_list = []
    contador_ransomware = 0
    api_url = "https://mb-api.abuse.ch/api/v1/"

    for hash in hashes:
        contador_ransomware += 1
        data = {
            "query": "get_info",
            "hash": hash
        }
        response = requests.post(api_url, data=data)
        if response.status_code == 200:
            try:
                if contador_ransomware%1000 == 0:
                        print(f"Se han procesado {contador_ransomware} hashes")
                if "Ransomware" in response.json()["data"][0]["tags"]:
                    write_valid_to_txt(hash)
                    
            except:
                print("Error")

        else:
            pass
    return resulted_list

# guarda los hashes pertenecientes a un ransomware
def write_valid_to_txt(hash):
    with open("ransomware_hashes.txt", "a", newline="", encoding="utf-8") as archivo:
        archivo.write(str(hash)+'\n')

def main():
    tiempo_inicio = time.time()
    contador_hashes = 0
    lista_hashes = []
    # lectura del fichero con los 900K hashes
    with open('hashes.txt', 'r') as file:
        for line in file:
            contador_hashes += 1
            # este contador se añadio por unas interrupciones en la ejecución, no es relevante
            if contador_hashes > 172027:
                hash_str = line.strip()  # Eliminar los espacios en blanco al inicio y al final de la línea
                lista_hashes.append(hash_str)

    search_malware_bazaar(lista_hashes)
    tiempo_fin = time.time()
    tiempo_transcurrido = tiempo_fin - tiempo_inicio
    print("Tiempo de ejecución:", tiempo_transcurrido, "segundos")

if __name__ == "__main__":
    main()
