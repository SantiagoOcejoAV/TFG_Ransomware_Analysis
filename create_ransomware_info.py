import requests
import csv
import time

# Funcion de busqueda en malawarebazaar
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
                resulted_list.append(response.json()["data"])
                    
            except:
                print("ERROR")

        else:
            pass
    return resulted_list

# funcion para escribir los resultados en un csv
def write_to_csv(results):
    with open("ransomware_info.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["File Name", "SHA256 Hash", "Type", "Signature","Tags", "Size", "First Seen", "Last Seen"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            
            writer.writerow({
                "File Name": result[0]["file_name"],
                "SHA256 Hash": result[0]["sha256_hash"],
                "Type": result[0]["file_type"],
                "Signature": result[0]["signature"],
                "Tags": result[0]["tags"],
                "Size": result[0]["file_size"],
                "First Seen": result[0]["first_seen"],
                "Last Seen": result[0]["last_seen"]
            })

# funcion main
def main():
    tiempo_inicio = time.time()
    contador_hashes = 0
    lista_hashes = []
    # lectura del fichero que contiene los hashes
    with open('hashes_finales.txt', 'r') as file:
        for line in file:
            contador_hashes += 1
            hash_str = line.strip()  # Eliminar los espacios en blanco al inicio y al final de la línea
            lista_hashes.append(hash_str)

    # se buscan los hashes y se recupera su informacion
    results = search_malware_bazaar(lista_hashes)
    print(f"Se encontraron {len(results)} resultados para la búsqueda.")
    write_to_csv(results)
    tiempo_fin = time.time()
    tiempo_transcurrido = tiempo_fin - tiempo_inicio
    print("Tiempo de ejecución:", tiempo_transcurrido, "segundos")

if __name__ == "__main__":
    main()
