#!/bin/sh

# Primero inicia Ollama en segundo plano
/bin/ollama serve &

# Espera 5 segundos a que el servicio esté listo
sleep 5

# Descarga el modelo si no existe
if ! ollama list | grep -q tinyllama; then
    echo "🔍 Descargando TinyLlama (500MB)..."
    ollama pull tinyllama
fi

# Mantén el contenedor en ejecución
wait
