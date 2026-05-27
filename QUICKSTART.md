# 🚀 Guía Rápida - Huffman Compressor Pro

## Inicio Rápido (5 minutos)

### Opción 1: Docker (Más fácil)

```bash
# 1. Clonar
git clone <url>
cd huffman-compressor-pro

# 2. Ejecutar
docker-compose up

# 3. Abrir navegador
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

### Opción 2: Local sin Docker

#### En Windows:
```bash
# 1. Ejecutar script
setup.bat

# 2. Terminal 1 - Backend
cd backend
venv\Scripts\activate.bat
uvicorn main:app --reload

# 3. Terminal 2 - Frontend
cd frontend
npm run dev
```

#### En Linux/Mac:
```bash
# 1. Ejecutar script
bash setup.sh

# 2. Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# 3. Terminal 2 - Frontend
cd frontend
npm run dev
```

## URLs Principales

| Componente | URL | Descripción |
|-----------|-----|-------------|
| Frontend | http://localhost:3000 | Aplicación web |
| Backend | http://localhost:8000 | API REST |
| Documentación | http://localhost:8000/docs | Swagger Interactive |
| ReDoc | http://localhost:8000/redoc | Documentación alternativa |

## Pruebas Rápidas

### Backend
```bash
cd backend
source venv/bin/activate  # o venv\Scripts\activate.bat
pytest tests/             # Ejecutar todas las pruebas
pytest tests/test_huffman.py::TestHuffmanAlgorithm::test_encode_decode -v
```

### Frontend
```bash
cd frontend
npm run build   # Compilar
npm run lint    # Lint
npm run type-check  # Verificar tipos
```

## Estructura de Carpetas

```
frontend/        → Aplicación web (Next.js)
backend/         → API REST (FastAPI)
docker-compose.yml  → Ejecución con Docker
.env.example     → Variables de entorno
README.md        → Documentación completa
```

## Desarrollo

### Editar Frontend
- Archivos en `frontend/components/` se recargan automáticamente
- Estilos en `frontend/app/globals.css`
- Tipos en `frontend/types/index.ts`

### Editar Backend
- Endpoints en `backend/app/api/routes/`
- Lógica en `backend/app/services/`
- Algoritmo en `backend/app/core/`

## Troubleshooting

| Problema | Solución |
|----------|----------|
| Puerto 3000 ocupado | `lsof -ti:3000 \| xargs kill -9` |
| Puerto 8000 ocupado | `lsof -ti:8000 \| xargs kill -9` |
| "Cannot GET /" | Esperar a que se compile Next.js |
| CORS error | Asegurarse que backend está en puerto 8000 |
| Módulos no encontrados | Ejecutar `npm install` o `pip install -r requirements.txt` |

## Características Principales

✅ Compresión Huffman  
✅ Interfaz moderna dark mode  
✅ Métricas académicas  
✅ Visualización de datos  
✅ Descarga de archivos  
✅ API REST documentada  
✅ Totalmente responsive  
✅ Soporte Unicode  

## Próximos Pasos

1. Abre http://localhost:3000
2. Sube un archivo .txt o escribe texto
3. Visualiza las métricas y gráficos
4. Descarga el archivo comprimido .huff
5. Sube el .huff para verificar descompresión

¡Listo! Ya estás comprimiendo con Huffman 🎉
