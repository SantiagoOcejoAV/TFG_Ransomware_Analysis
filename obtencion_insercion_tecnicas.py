import requests
import mysql.connector
from mysql.connector import Error
import time
import json

diccionario_tecnicas = {}

def leer_hashes_desde_archivo(ruta_archivo):
    hashes = []
    try:
        with open(ruta_archivo, 'r') as archivo:
            for linea in archivo:
                hash = linea.strip()  # Elimina cualquier espacio en blanco al principio y al final
                if id:  # Solo añade si la línea no está vacía
                    hashes.append(hash)
    except FileNotFoundError:
        print(f"El archivo {ruta_archivo} no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
    return hashes

# Verificar si la columna existe antes de agregarla
def agregar_columna_si_no_existe(cursor, tabla, columna):
    cursor.execute(f"SHOW COLUMNS FROM tactica_{tabla} LIKE '{columna}'")
    resultado = cursor.fetchone()
    if not resultado:
        cursor.execute(f"ALTER TABLE tactica_{tabla} ADD COLUMN {columna} TINYINT(1) DEFAULT 0")


def tecnicas_mittre():
    contador_consultas = 0
    tiempo_inicio = time.time()
    
    ruta_archivo_hashes = 'hashes_finales.txt'
    hashes = leer_hashes_desde_archivo(ruta_archivo_hashes)

    headers = {
    "accept": "application/json",
    "x-apikey": "7fbd68919b60a5eb8ea54c00f6016b7951aec541e282d176515f63f862451687"
    }
    

    for hash in hashes:
        contador_consultas = contador_consultas +1
        url = "https://www.virustotal.com/api/v3/files/"+hash+"/behaviour_mitre_trees"


        if contador_consultas > 4:
            tiempo_fin_cuatro = time.time()
            tiempo_transcurrido = tiempo_fin_cuatro - tiempo_inicio
            print("Tiempo de ejecución:", tiempo_transcurrido, "segundos")

        response = requests.get(url, headers=headers)

        try:
            diccionario_tecnicas[hash] = {}
            extraer_tecnicas(response.json(),hash)
            
    
        except:
            print("Error en el hash: "+hash+"\n")
            print(response.text)
            break



def extraer_tecnicas(data,hash):

    for item in data['data']:
        for tactic in data['data'][item]['tactics']:
            diccionario_tecnicas[hash][tactic['id']] = []
            for technique in tactic['techniques']:
                variable = technique['id']
                if '.' in variable:
                    # Reemplazar el punto por $, ya que si no, SQL da problemas
                    variable = variable.replace('.', '$')
                    diccionario_tecnicas[hash][tactic['id']].append(variable)
                else:
                    diccionario_tecnicas[hash][tactic['id']].append(technique['id'])

def create_connection(host_name, user_name, user_password, db_name):
    """ Crea una conexión a la base de datos MySQL """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
    except Error as e:
        pass

    return connection

def insertar_tecnicas(host_name, user_name, user_password,db_name):  

    conn = create_connection(host_name, user_name, user_password, db_name)
    cursor = conn.cursor()

    for hash_value, tacticas in diccionario_tecnicas.items():
        for tactica, tecnicas in tacticas.items():
            for tecnica in tecnicas:
                agregar_columna_si_no_existe(cursor, tactica, tecnica)

            # Preparar columnas y valores para la inserción
            tecnica_columns = ', '.join(tecnicas)
            tecnica_values = ', '.join(['1'] * len(tecnicas))
            cursor.execute(f"INSERT INTO tactica_{tactica} (hash, {tecnica_columns}) VALUES (%s, {tecnica_values}) ON DUPLICATE KEY UPDATE " +
                        ', '.join([f"{tecnica} = 1" for tecnica in tecnicas]), (hash_value,))

def main():
    host_name = 'localhost' 
    user_name = 'root' 
    user_password = '' 
    db_name = 'hashes_ransomware'
    
    tecnicas_mittre()
    insertar_tecnicas(host_name, user_name, user_password,db_name)
    

if __name__ == "__main__":
    main()
