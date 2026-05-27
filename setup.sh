#!/bin/bash

# Huffman Compressor Pro - Script de Ejecución

set -e

echo "═══════════════════════════════════════════"
echo "  Huffman Compressor Pro - Setup"
echo "═══════════════════════════════════════════"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js no está instalado"
    exit 1
fi

echo "✅ Python: $(python3 --version)"
echo "✅ Node.js: $(node --version)"
echo "✅ npm: $(npm --version)"
echo ""

# Backend
echo "📦 Configurando Backend..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt -q

cd ..

# Frontend
echo "📦 Configurando Frontend..."
cd frontend

npm install -q

cd ..

echo ""
echo "═══════════════════════════════════════════"
echo "  ✅ Setup Completado"
echo "═══════════════════════════════════════════"
echo ""
echo "Para ejecutar la aplicación:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --reload"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "Docs API: http://localhost:8000/docs"
echo ""
