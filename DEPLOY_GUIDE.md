# Guía Paso a Paso para Desplegar en Railway

## Paso 1: Crear cuenta en Railway
1. Ve a https://railway.app
2. Haz clic en "Get Started"
3. Regístrate con GitHub (recomendado) o con email
4. Confirma tu cuenta desde el email que recibirás

## Paso 2: Subir código a GitHub
1. Crea un nuevo repositorio en GitHub: https://github.com/new
2. Nombre: `sunarp-api` (o el nombre que prefieras)
3. Descripción: "API para consultar datos de vehículos SUNARP"
4. **IMPORTANTE**: No marques "Initialize this repository with a README"
5. Haz clic en "Create repository"

## Paso 3: Subir el código (SIN la base de datos)
```bash
# Inicializar git
git init

# Agregar todos los archivos excepto la base de datos
git add .

# Hacer commit
git commit -m "Initial commit: SUNARP API"

# Configurar el repositorio remoto
git branch -M main
git remote add origin https://github.com/tu-usuario/sunarp-api.git

# Subir el código
git push -u origin main
```

## Paso 4: Conectar Railway con GitHub
1. En Railway, haz clic en "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Conecta tu cuenta de GitHub si no lo has hecho
4. Busca tu repositorio `sunarp-api` y haz clic en "Connect"
5. Railway detectará automáticamente que es Python y comenzará el despliegue

## Paso 5: Configurar variable de entorno
1. En Railway, ve a tu proyecto
2. Haz clic en "Variables"
3. Agrega una nueva variable:
   - **Nombre**: `DATABASE_URL`
   - **Valor**: `https://drive.google.com/uc?export=download&id=1Izo_ua3vIkyFgyOv7gjCoAbKvLEGJRub`
4. Haz clic en "Add"

## Paso 6: Verificar el despliegue
1. Railway mostrará la URL de tu API (ej: https://sunarp-api.up.railway.app)
2. La API descargará automáticamente la base de datos al iniciar
3. Puedes probar los endpoints:
   - `https://tu-proyecto.railway.app/placa/ABC123`
   - `https://tu-proyecto.railway.app/tarjeta/4070673`

## Notas importantes:
- El despliegue inicial puede tardar unos minutos (especialmente la descarga de la base de datos)
- Railway ofrece 500 horas gratuitas por mes
- La API estará disponible 24/7
- Puedes monitorear el uso y logs desde el dashboard de Railway

## Solución de problemas:
- Si falla la descarga, verifica que el enlace de Google Drive sea público
- Revisa los logs en Railway para ver errores específicos
- La variable `DATABASE_URL` debe tener el formato correcto de Google Drive

¡Tu API estará funcionando en producción en minutos!
