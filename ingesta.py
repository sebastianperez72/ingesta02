import os
import csv
import boto3
import pymysql

# Parametros (se pueden cambiar con variables de entorno)
DB_HOST = os.getenv("DB_HOST", "mysql_c")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "utec")
DB_NAME = os.getenv("DB_NAME", "tienda")
DB_TABLE = os.getenv("DB_TABLE", "clientes")

ficheroUpload = "data.csv"
nombreBucket = os.getenv("BUCKET", "gcr-output-02")  # <-- reemplace por su bucket

# 1. Conectarse a MySQL y leer todos los registros de la tabla
conexion = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER,
                           password=DB_PASSWORD, database=DB_NAME)
cursor = conexion.cursor()
cursor.execute(f"SELECT * FROM {DB_TABLE}")
registros = cursor.fetchall()
columnas = [c[0] for c in cursor.description]
cursor.close()
conexion.close()
print(f"Registros leidos de {DB_NAME}.{DB_TABLE}: {len(registros)}")

# 2. Guardar los registros en un archivo CSV
with open(ficheroUpload, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(columnas)
    writer.writerows(registros)
print(f"Archivo {ficheroUpload} generado")

# 3. Subir el CSV al bucket S3
s3 = boto3.client("s3")
s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)

print("Ingesta completada")
