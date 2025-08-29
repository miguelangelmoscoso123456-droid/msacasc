# Instrucciones para subir la base de datos

## Problema
GitHub tiene un límite de 25MB por archivo, pero nuestra base de datos Sunarp.db pesa 837MB.

## Solución
Debes subir la base de datos a un servicio de almacenamiento en la nube y configurar la URL en Railway.

### Opción 1: Google Drive (Recomendado)
1. Sube el archivo `Sunarp.db` a Google Drive
2. Haz clic derecho en el archivo y selecciona "Obtener enlace"
3. Cambia los permisos a "Cualquier persona con el enlace"
4. Copia el enlace y reemplaza la parte final:
   - Original: `https://drive.google.com/file/d/ARCHIVE_ID/view?usp=sharing`
   - Para descargar: `https://drive.google.com/uc?export=download&id=ARCHIVE_ID`

### Opción 2: Dropbox
1. Sube el archivo a Dropbox
2. Haz clic derecho → Compartir → Crear enlace
3. Cambia el final del enlace de `?dl=0` a `?dl=1`
   - Ejemplo: `https://www.dropbox.com/s/ARCHIVE_ID/Sunarp.db?dl=1`

### Opción 3: Servidor propio
Si tienes un servidor, sube el archivo y obtén una URL directa.

## Configuración en Railway
1. Después de desplegar en Railway, ve a la sección "Variables"
2. Agrega una variable de entorno:
   - **Nombre**: `DATABASE_URL`
   - **Valor**: La URL de descarga de tu base de datos

## Ejemplo de URLs válidas:
- Google Drive: `https://drive.google.com/uc?export=download&id=1ABC123def456GHI789jkl`
- Dropbox: `https://www.dropbox.com/s/abcdef123456/Sunarp.db?dl=1`
- Servidor propio: `https://tudominio.com/Sunarp.db`

## Nota importante
La API descargará automáticamente la base de datos cuando se inicie en Railway usando la URL que configures.
