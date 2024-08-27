import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# Parámetros de conexión
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'hashes_ransomware'
TABLE_NAME = 'info_general'

# Cargar el CSV en un DataFrame de pandas
csv_file_path = './ransomware_info.csv'
df = pd.read_csv(csv_file_path)

# Limpiar la columna 'tags' para eliminar corchetes y comillas
df['Tags'] = df['Tags'].str.replace(r"[\'\[\]]", '', regex=True)

# Conectar a la base de datos
engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# Guardar el DataFrame como una nueva tabla en la base de datos
df.to_sql(TABLE_NAME, con=engine, if_exists='replace', index=False)

print(f"Datos del CSV replicados en la tabla '{TABLE_NAME}' exitosamente.")
