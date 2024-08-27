
## Ficheros y Funciones del Proyecto

### Scripts
- **filtrado_hashes_ransomware**: Procesa el fichero con los 900K hashes y filtra solo aquellos que pertenecen a ransomwares.
- **create_ransomware_info**: Recopila información (tags, tamaños, tipo, etc.) de los hashes finales y la almacena en un archivo `.csv`.
- **create_tabla_info_general**: Utiliza la información del script anterior para crear una tabla en la base de datos con la información general de cada hash.
- **obtención_insercion_tacticas**: Extrae todas las tácticas utilizadas por los hashes recopilados e inserta esta información en la tabla `hashes_tactics`.
- **create_tabla_individual_tacticas**: Crea una tabla individual para cada táctica. Cada tabla contiene las técnicas asociadas y marca con '1' o '0' los ransomwares que las utilizan.
- **obtención_insercion_tecnicas**: Extrae las técnicas utilizadas por los hashes y las inserta en la tabla correspondiente a la táctica asociada.

### Archivos de Datos
- **hashes.zip**: Contiene un fichero .txt con todos los hashes proporcionados por MalwareBazaar.
- **ransomware_hashes.txt**: Incluye los hashes que pertenecen a malware de tipo ransomware.
- **hashes_finales.txt**: Almacena los hashes que poseen información relativa a MITRE (tácticas y técnicas).

### Otros
- **tiempo_ejecucion.txt**: Documenta la cantidad de tiempo que supuso extraer los ransomware de entre todos los hashes de malware.
