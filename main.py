from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List, Optional
import os
import urllib.request
import tempfile

app = FastAPI(
    title="SUNARP API",
    description="API para consultar datos de vehículos de SUNARP",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variable global para la conexión a la base de datos
_db_connection = None
_db_path = None

def get_db_connection():
    global _db_connection, _db_path
    
    if _db_connection is None:
        # En producción, descargar la base de datos desde una URL
        if os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("DATABASE_URL"):
            # Crear directorio temporal para la base de datos
            temp_dir = tempfile.mkdtemp()
            _db_path = os.path.join(temp_dir, "Sunarp.db")
            
            # URL de la base de datos desde Google Drive con confirmación
            db_url = os.environ.get("DATABASE_URL", "https://drive.usercontent.google.com/download?id=1Izo_ua3vIkyFgyOv7gjCoAbKvLEGJRub&export=download&pli=1&authuser=0&confirm=t&uuid=31374f0f-a34f-4898-9d15-409c4f2c49a1&at=AN8xHoo3cpJVUbwkhm53pV2gXFnb%3A1756475097337")
            
            try:
                # Descargar la base de datos
                print(f"Descargando base de datos desde: {db_url}")
                urllib.request.urlretrieve(db_url, _db_path)
                
                # Verificar que el archivo se descargó correctamente
                file_size = os.path.getsize(_db_path)
                print(f"Base de datos descargada exitosamente. Tamaño: {file_size} bytes")
                
                # Verificar que es un archivo SQLite válido
                try:
                    test_conn = sqlite3.connect(_db_path)
                    test_cursor = test_conn.cursor()
                    test_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = test_cursor.fetchall()
                    print(f"Tablas encontradas en la base de datos: {tables}")
                    test_conn.close()
                except Exception as db_error:
                    print(f"Error verificando base de datos: {db_error}")
                    raise Exception(f"El archivo descargado no es una base de datos SQLite válida: {db_error}")
                    
            except Exception as e:
                print(f"Error descargando base de datos: {e}")
                # Crear base de datos vacía como fallback
                open(_db_path, 'wb').close()
                print("Base de datos vacía creada como fallback")
        else:
            # Desarrollo local - usar archivo local
            _db_path = 'Sunarp.db'
        
        _db_connection = sqlite3.connect(_db_path)
        _db_connection.row_factory = sqlite3.Row
        
        # Crear índices si no existen
        create_indexes(_db_connection)
    
    return _db_connection

# Crear índices para optimizar consultas
def create_indexes(conn):
    try:
        # Índice para búsqueda por placa
        conn.execute("CREATE INDEX IF NOT EXISTS idx_placa ON data(placa)")
        # Índice para búsqueda por número de registro
        conn.execute("CREATE INDEX IF NOT EXISTS idx_nro_registro ON data(nro_registro)")
        # Índice para búsqueda por VIN
        conn.execute("CREATE INDEX IF NOT EXISTS idx_vin ON data(vin)")
        # Índice para búsqueda por tarjeta
        conn.execute("CREATE INDEX IF NOT EXISTS idx_tarjeta ON data(tarjeta)")
        conn.commit()
        print("Índices creados exitosamente")
    except Exception as e:
        print(f"Error creando índices: {e}")

# Crear índices al iniciar la aplicación
@app.on_event("startup")
async def startup_event():
    # La conexión se crea automáticamente al primer uso
    # Los índices se crean en get_db_connection()
    pass

@app.get("/")
async def root():
    return {"message": "API SUNARP - Sistema de consulta de vehículos"}

@app.get("/data")
async def get_data(
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(50, ge=1, le=100, description="Límite de registros por página")
):
    conn = get_db_connection()
    try:
        offset = (page - 1) * limit
        cursor = conn.cursor()
        
        # Obtener total de registros
        cursor.execute("SELECT COUNT(*) as total FROM data")
        total_records = cursor.fetchone()["total"]
        
        # Obtener datos paginados
        cursor.execute(
            "SELECT * FROM data LIMIT ? OFFSET ?",
            (limit, offset)
        )
        
        records = [dict(row) for row in cursor.fetchall()]
        
        return {
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "total_pages": (total_records + limit - 1) // limit,
            "data": records
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")
    finally:
        conn.close()

@app.get("/data/{placa}")
async def get_by_placa(placa: str):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM data WHERE placa = ?",
            (placa.upper(),)
        )
        
        record = cursor.fetchone()
        if record is None:
            raise HTTPException(status_code=404, detail="Placa no encontrada")
        
        return dict(record)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar placa: {str(e)}")
    finally:
        conn.close()

@app.get("/search")
async def search_data(
    q: str = Query(..., description="Término de búsqueda"),
    field: str = Query("placa", description="Campo a buscar (placa, nro_registro, vin, marca, modelo, titular)"),
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(50, ge=1, le=100, description="Límite de registros por página")
):
    valid_fields = ["placa", "nro_registro", "vin", "marca", "modelo", "titular"]
    if field not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Campo inválido. Campos válidos: {', '.join(valid_fields)}")
    
    conn = get_db_connection()
    try:
        offset = (page - 1) * limit
        cursor = conn.cursor()
        
        # Contar total de registros que coinciden
        cursor.execute(
            f"SELECT COUNT(*) as total FROM data WHERE {field} LIKE ?",
            (f"%{q}%",)
        )
        total_records = cursor.fetchone()["total"]
        
        # Obtener datos paginados
        cursor.execute(
            f"SELECT * FROM data WHERE {field} LIKE ? LIMIT ? OFFSET ?",
            (f"%{q}%", limit, offset)
        )
        
        records = [dict(row) for row in cursor.fetchall()]
        
        return {
            "query": q,
            "field": field,
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "total_pages": (total_records + limit - 1) // limit,
            "data": records
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")
    finally:
        conn.close()

@app.get("/placa/{placa}")
async def get_by_placa_exact(placa: str):
    """Buscar vehículo por placa exacta"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM data WHERE placa = ?",
            (placa.upper(),)
        )
        
        record = cursor.fetchone()
        if record is None:
            raise HTTPException(status_code=404, detail="Placa no encontrada")
        
        return dict(record)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar placa: {str(e)}")
    finally:
        conn.close()

@app.get("/tarjeta/{tarjeta}")
async def get_by_tarjeta(tarjeta: str):
    """Buscar vehículos por número de tarjeta"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM data WHERE tarjeta = ?",
            (tarjeta,)
        )
        
        records = [dict(row) for row in cursor.fetchall()]
        if not records:
            raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
        
        return {
            "tarjeta": tarjeta,
            "total_vehiculos": len(records),
            "data": records
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar por tarjeta: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
