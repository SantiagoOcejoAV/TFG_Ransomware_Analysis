import requests
import mysql.connector
from mysql.connector import Error
import time


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

#función para extraer las tácticas
def extraer_tacticas(data):
    ids = []
    
    for item in data['data']:
        for tactic in data['data'][item]['tactics']:
            ids.append(tactic['id'])
    return ids



def create_connection(host_name, user_name, user_password, db_name):
    """ Crea una conexión a la base de datos """
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

def check_and_create_columns(conn, table, ids):
    """ Verifica si las columnas existen y si no, las crea """
    cursor = conn.cursor()
    for column in ids:
        cursor.execute(f"SHOW COLUMNS FROM {table} LIKE '{column}'")
        result = cursor.fetchone()
        if not result:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} INT DEFAULT 0")
    conn.commit()

def check_and_create_rows(conn, table, hash):
    try:
        cursor = conn.cursor()

        # Verificar si ya existe una fila con el hash dado
        cursor.execute(f"SELECT * FROM {table} WHERE hash = '{hash}'")
        result = cursor.fetchone()

        if not result:
            # Si no existe, crear la nueva fila con valores predeterminados
            cursor.execute(f"INSERT INTO {table} (hash) VALUES ('{hash}')")

        conn.commit()

    except Error as e:
        #print(f"Error al conectar a MySQL en el metodo: {e}")
        pass

def update_row_with_ids(conn, table, hash_value, ids):
    """ Actualiza la fila correspondiente con los valores de las columnas establecidas en 1 """
    cursor = conn.cursor()
    set_clause = ', '.join([f"{id} = 1" for id in ids])
    cursor.execute(f"UPDATE {table} SET {set_clause} WHERE hash = %s", (hash_value,))
    conn.commit()

def obtener_hashes_sin_tecnicas(host_name, user_name, user_password, db_name):
    conn = create_connection(host_name, user_name, user_password, db_name)
    cursor = conn.cursor()

    # Consulta SQL para obtener los hashes cuyos valores para los 10 primeros id sean 1
    query = """
        SELECT hash
        FROM hashes_tactics
        WHERE TA0005 = 0 AND TA0007 = 0 AND TA0034 = 0 AND TA0040 = 0 AND TA0009 = 0
        AND TA0002 = 0 AND TA0003 = 0 AND TA0004 = 0 AND TA0006 = 0 AND TA0011 = 0
        AND TA0001 = 0 AND TA0008 = 0 AND TA0030 = 0 AND TA0032 = 0 AND TA0031 = 0
        AND TA0035 = 0 AND TA0010 = 0 AND TA0043 = 0
        """
    cursor.execute(query)

    # Obtención de los resultados
    hashes = cursor.fetchall()

    # Cierre de la conexión a la base de datos
    cursor.close()
    conn.close()

    # Guardar los hashes en un .txt
    with open('hashes_invalidos.txt', 'w') as file:
        for hash_tuple in hashes:
            file.write(f"{hash_tuple[0]}\n")

def insertar_hashes_tacticas(host_name, user_name, user_password, db_name):
    contador_consultas = 0
    tiempo_inicio = time.time()
    """host_name = host_name  # Reemplaza con el host de tu base de datos MySQL
    user_name = user_name  # Reemplaza con tu usuario de MySQL
    user_password = user_password  # Reemplaza con tu contraseña de MySQL
    db_name = db_name # Reemplaza con el nombre de tu base de datos"""
    table = 'hashes_tactics'
    
    ruta_archivo_hashes = 'ransomware_hashes.txt'
    hashes = leer_hashes_desde_archivo(ruta_archivo_hashes)

    headers = {
    "accept": "application/json",
    "x-apikey": "8c601962ac2162ee5c1ef13e2dd37a357d1da00d41e144b415fbd52bf5dd8b08"
    }
    

    for hash in hashes:
        contador_consultas = contador_consultas +1
        url = "https://www.virustotal.com/api/v3/files/"+hash+"/behaviour_mitre_trees"

        # conexión a la base de datos
        conn = create_connection(host_name, user_name, user_password, db_name)

        if contador_consultas > 4:
            tiempo_fin_cuatro = time.time()
            tiempo_transcurrido = tiempo_fin_cuatro - tiempo_inicio
            print("Tiempo de ejecución:", tiempo_transcurrido, "segundos")

        response = requests.get(url, headers=headers)

        try:
            tacticas = extraer_tacticas(response.json())
        except:
            print("Error en el hash: "+hash+"\n")
            print(response.text)
            break
        
        if conn:
            with conn:
                # Verifica si las columnas existen y si no, las crea
                if tacticas:
                    check_and_create_columns(conn, table, tacticas)
                
                check_and_create_rows(conn, table, hash)
                # Actualiza la fila correspondiente con los valores de las columnas establecidas en 1
                if tacticas:
                    update_row_with_ids(conn, table, hash, tacticas)

    #cálculo del tiempo de ejecución               
    tiempo_fin = time.time()
    tiempo_transcurrido = tiempo_fin - tiempo_inicio
    print("Tiempo de ejecución:", tiempo_transcurrido, "segundos")

def main():
    host_name = 'localhost'
    user_name = 'root'
    user_password = ''
    db_name = 'hashes_ransomware'
    insertar_hashes_tacticas(host_name, user_name, user_password,db_name)
    

if __name__ == "__main__":
    main()
