# Guía de Despliegue en Render

## Pasos para desplegar en Render:

1. **Crear cuenta en Render**
   - Ve a https://render.com
   - Regístrate con tu cuenta de GitHub

2. **Conectar repositorio**
   - Haz click en "New +" → "Web Service"
   - Conecta tu cuenta de GitHub
   - Selecciona el repositorio `msacasc`

3. **Configurar el servicio**
   - **Name**: `sunarp-api`
   - **Environment**: `Python`
   - **Region**: `Oregon (us-west)` (recomendado para mejor performance)
   - **Branch**: `main`
   - **Root Directory**: `.` (dejar vacío)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`

4. **Variables de entorno**
   - **DATABASE_URL**: `https://drive.usercontent.google.com/download?id=1Izo_ua3vIkyFgyOv7gjCoAbKvLEGJRub&export=download&pli=1&authuser=0&confirm=t&uuid=31374f0f-a34f-4898-9d15-409c4f2c49a1&at=AN8xHoo3cpJVUbwkhm53pV2gXFnb%3A1756475097337`

5. **Plan**
   - Selecciona el plan **Free**

6. **Desplegar**
   - Haz click en "Create Web Service"
   - Render comenzará el proceso de despliegue automáticamente

## Ventajas de Render vs Railway:

- **Mejor rendimiento** para aplicaciones con bases de datos grandes
- **1GB de almacenamiento** gratis
- **Mejor uptime** y velocidad de respuesta
- **Despliegue continuo** desde GitHub

## Notas importantes:

- El primer despliegue puede tardar unos minutos mientras descarga la base de datos
- Render tiene un timeout de build de 45 minutos, suficiente para descargar 1GB
- Los logs estarán disponibles en el dashboard de Render para monitorear

## URLs después del despliegue:

- **API**: `https://sunarp-api.onrender.com`
- **Documentación**: `https://sunarp-api.onrender.com/docs`
- **Dashboard**: https://dashboard.render.com

## Monitoreo:

Revisa los logs en el dashboard de Render para:
- Ver el progreso de la descarga de la base de datos
- Monitorear errores o problemas de rendimiento
- Verificar que los índices se creen correctamente
