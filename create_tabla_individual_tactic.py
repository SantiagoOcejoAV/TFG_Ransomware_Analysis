# SCRIPT PARA LA CREACION DE LAS TABLAS INDIVIDUALES DE CADA TACTICA


import pandas as pd
import mysql.connector

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hashes_ransomware"
)

# Cargamos la tabla original
query = "SELECT * FROM hashes_tactics"  
tabla_original = pd.read_sql(query, conn)

# Cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Recorremos cada columna
for id_col in tabla_original.columns[1:]:  # Ignoramos la primera columna que contiene los hashes
    # Filtramos los hashes que tienen un valor 1 en la columna actual
    hashes_asociados = tabla_original[tabla_original[id_col] == 1]['hash']
    
    # Nombre de la nueva tabla
    nombre_tabla = f'tactica_{id_col}'
    
    # Crear la nueva tabla
    cursor.execute(f"DROP TABLE IF EXISTS {nombre_tabla}")
    cursor.execute(f"""
        CREATE TABLE {nombre_tabla} (
            hash VARCHAR(255)
        )
    """)
    
    # Insertar los hashes en la nueva tabla
    for hash_val in hashes_asociados:
        cursor.execute(f"INSERT INTO {nombre_tabla} (hash) VALUES (%s)", (hash_val,))
    
    # Guardar los cambios
    conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()

print("Tablas generadas correctamente.")
