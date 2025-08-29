#!/bin/bash
echo "=== Configuración inicial para despliegue en Railway ==="

# Verificar si ya existe un repositorio git
if [ ! -d ".git" ]; then
    echo "Inicializando repositorio git..."
    git init
    git add .
    git commit -m "Initial commit: SUNARP API con FastAPI"
    echo "✅ Repositorio git inicializado"
else
    echo "⚠️  Ya existe un repositorio git"
    git status
fi

echo ""
echo "=== INSTRUCCIONES FINALES ==="
echo "1. Crea un repositorio en GitHub: https://github.com/new"
echo "2. No marques 'Initialize with README'"
echo "3. Ejecuta estos comandos:"
echo ""
echo "git branch -M main"
echo "git remote add origin https://github.com/TU_USUARIO/sunarp-api.git"
echo "git push -u origin main"
echo ""
echo "4. Conecta Railway a tu repositorio GitHub"
echo "5. Configura la variable DATABASE_URL en Railway"
echo ""
echo "¡Tu API estará en producción!"
