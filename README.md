# API SUNARP - Sistema de Consulta de Vehículos

API REST construida con FastAPI para consultar datos de vehículos de la base de datos SUNARP.

## Características

- Consulta paginada de registros
- Búsqueda por placa específica
- Búsqueda flexible por diferentes campos
- Optimizada con índices SQLite
- Documentación automática con Swagger UI

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Asegúrate de tener el archivo `Sunarp.db` en el mismo directorio

## Ejecución local

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: http://localhost:8000

## Documentación

- **Swagger UI**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

## Endpoints

### GET /
Información básica de la API

### GET /data
Obtiene registros paginados

**Parámetros:**
- `page` (opcional): Número de página (default: 1)
- `limit` (opcional): Límite de registros por página (max: 100, default: 50)

**Ejemplo:**
```bash
GET /data?page=1&limit=10
```

### GET /data/{placa}
Obtiene un registro específico por placa

**Ejemplo:**
```bash
GET /data/ABC123
```

### GET /search
Búsqueda flexible por diferentes campos

**Parámetros:**
- `q` (requerido): Término de búsqueda
- `field` (opcional): Campo a buscar (placa, nro_registro, vin, marca, modelo)
- `page` (opcional): Número de página
- `limit` (opcional): Límite de registros

**Ejemplos:**
```bash
GET /search?q=Toyota&field=marca&page=1&limit=10
GET /search?q=123456&field=nro_registro
GET /search?q=ABC123&field=placa
```

## Estructura de la Base de Datos

La tabla `data` contiene las siguientes columnas:
- placa (TEXT)
- nro_registro (TEXT)
- nro_sede (TEXT)
- color (TEXT)
- estado (TEXT)
- marca (TEXT)
- modelo (TEXT)
- motor (TEXT)
- serie (TEXT)
- vin (TEXT)
- anterior (TEXT)
- vidente (TEXT)
- titulares (TEXT)
- nro_titulares (TEXT)
- sede (TEXT)
- tarjeta (TEXT)
- titular (TEXT)
- oficina (TEXT)
- creado (TEXT)
- actualizado (TEXT)
- deuda_papeletas (TEXT)
- nro_papeletas (TEXT)
- soats (TEXT)
- fabricacion (TEXT)

## Despliegue en Railway

### Pasos para desplegar:

1. **Subir el proyecto a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: SUNARP API"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/sunarp-api.git
   git push -u origin main
   ```

2. **Crear cuenta en Railway:**
   - Ve a https://railway.app y crea una cuenta gratuita
   - Conecta tu cuenta de GitHub

3. **Desplegar desde GitHub:**
   - En Railway, haz clic en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio
   - Railway detectará automáticamente la configuración

4. **Configurar variables (si es necesario):**
   - Railway detectará automáticamente que es una aplicación Python
   - No se necesitan variables especiales para SQLite

5. **La API estará disponible en:**
   - https://tu-proyecto.railway.app

### Notas importantes:
- **NO** subas `Sunarp.db` a GitHub (está en .gitignore)
- Debes subir la base de datos a Google Drive, Dropbox u otro servicio
- Configura la variable `DATABASE_URL` en Railway con la URL de descarga
- Consulta `UPLOAD_DB_INSTRUCTIONS.md` para instrucciones detalladas
- La API descargará automáticamente la base de datos al iniciar
- La API estará disponible públicamente con una URL única de Railway

### Endpoints disponibles después del despliegue:
- `https://tu-proyecto.railway.app/placa/ABC123`
- `https://tu-proyecto.railway.app/tarjeta/4070673`
- `https://tu-proyecto.railway.app/data` (con paginación)
- `https://tu-proyecto.railway.app/search` (búsqueda flexible)

## Optimizaciones

- Índices creados automáticamente en campos de búsqueda frecuentes
- Paginación para manejar grandes volúmenes de datos (4M+ registros)
- Límites en consultas para prevenir sobrecarga
