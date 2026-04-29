from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from azure.storage.blob import BlobServiceClient
import psycopg2
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CONN_STR = os.getenv("AZURE_CONNECTION_STRING")
CONTAINER_LAB = os.getenv("AZURE_CONTAINER_LAB")
CONTAINER_IMG = os.getenv("AZURE_CONTAINER_IMG")

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "db",
    "port": "5432"
}

def get_db():
    return psycopg2.connect(**DB_CONFIG)

@app.on_event("startup")
def startup():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100),
            rut VARCHAR(20),
            tipo VARCHAR(20),
            archivo VARCHAR(200)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.get("/pacientes")
def listar_pacientes():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, rut, tipo, archivo FROM pacientes")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "nombre": r[1], "rut": r[2], "tipo": r[3], "archivo": r[4]} for r in rows]

@app.post("/subir/{tipo}")
async def subir_archivo(tipo: str, nombre: str, rut: str, file: UploadFile = File(...)):
    container = CONTAINER_LAB if tipo == "laboratorio" else CONTAINER_IMG
    blob_client = BlobServiceClient.from_connection_string(CONN_STR).get_blob_client(
        container=container, blob=file.filename
    )
    blob_client.upload_blob(await file.read(), overwrite=True)

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pacientes (nombre, rut, tipo, archivo) VALUES (%s, %s, %s, %s)",
        (nombre, rut, tipo, file.filename)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"mensaje": "Archivo subido exitosamente", "archivo": file.filename}

@app.get("/descargar/{tipo}/{filename}")
def descargar_archivo(tipo: str, filename: str):
    container = CONTAINER_LAB if tipo == "laboratorio" else CONTAINER_IMG
    blob_client = BlobServiceClient.from_connection_string(CONN_STR).get_blob_client(
        container=container, blob=filename
    )
    url = blob_client.url
    return {"url": url}
