"""
Main: Aplicación FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.compression import router as compression_router

# Crear aplicación
app = FastAPI(
    title="Huffman Compressor Pro API",
    description="API para comprimir y descomprimir archivos usando el algoritmo de Huffman",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(compression_router)


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Huffman Compressor Pro API",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
