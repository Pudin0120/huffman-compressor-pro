"""
API Routes: Endpoints FastAPI
"""

import uuid
import os
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from app.services.compression_service import CompressionService
from app.schemas.compression_schemas import (
    CompressResponseSchema,
    DecompressResponseSchema,
    ErrorResponseSchema
)

router = APIRouter(prefix="/api", tags=["compression"])

# Almacenamiento en memoria de sesiones (en producción usar base de datos)
sessions = {}


@router.get("/health")
async def health_check():
    """Verifica que el backend esté funcionando"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Huffman Compressor Pro"
    }


@router.post("/compress/text")
async def compress_text(text: str, filename: str = "file.txt"):
    """
    Comprime un texto usando el algoritmo de Huffman.
    
    Args:
        text: Texto a comprimir
        filename: Nombre del archivo (para metadatos)
        
    Returns:
        Métricas de compresión y ID de sesión
    """
    try:
        if not text:
            raise ValueError("El texto no puede estar vacío")
        
        if len(text) > 10_000_000:  # Límite de 10MB de caracteres
            raise ValueError("El archivo es demasiado grande (máx 10MB)")
        
        # Comprimir
        huff_bytes, metrics, visualization = CompressionService.compress_text(text, filename)
        
        # Guardar sesión
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "huff_bytes": huff_bytes,
            "original_text": text,
            "filename": filename,
            "metrics": metrics,
            "visualization": visualization
        }
        
        return CompressResponseSchema(
            success=True,
            session_id=session_id,
            original_size=metrics.original_size,
            compressed_size=metrics.compressed_size,
            compression_ratio=metrics.compression_ratio,
            shannon_entropy=metrics.shannon_entropy,
            average_code_length=metrics.average_code_length,
            efficiency=metrics.efficiency,
            unique_characters=metrics.unique_characters,
            characters_count=metrics.characters_count,
            compression_time=metrics.compression_time
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/compress/file")
async def compress_file(file: UploadFile = File(...)):
    """
    Comprime un archivo .txt.
    
    Args:
        file: Archivo .txt a comprimir
        
    Returns:
        Métricas de compresión
    """
    try:
        # Validar extensión
        if not file.filename.lower().endswith(".txt"):
            raise ValueError("Solo se aceptan archivos .txt")
        
        # Leer contenido
        content = await file.read()
        text = content.decode("utf-8")
        
        if not text.strip():
            raise ValueError("El archivo está vacío")
        
        # Comprimir
        huff_bytes, metrics, visualization = CompressionService.compress_text(text, file.filename)
        
        # Guardar sesión
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "huff_bytes": huff_bytes,
            "original_text": text,
            "filename": file.filename,
            "metrics": metrics,
            "visualization": visualization
        }
        
        return CompressResponseSchema(
            success=True,
            session_id=session_id,
            original_size=metrics.original_size,
            compressed_size=metrics.compressed_size,
            compression_ratio=metrics.compression_ratio,
            shannon_entropy=metrics.shannon_entropy,
            average_code_length=metrics.average_code_length,
            efficiency=metrics.efficiency,
            unique_characters=metrics.unique_characters,
            characters_count=metrics.characters_count,
            compression_time=metrics.compression_time
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/decompress/file")
async def decompress_file(file: UploadFile = File(...)):
    """
    Descomprime un archivo .huff.
    
    Args:
        file: Archivo .huff a descomprimir
        
    Returns:
        Información del archivo descomprimido
    """
    try:
        # Validar extensión
        if not file.filename.lower().endswith(".huff"):
            raise ValueError("Solo se aceptan archivos .huff")
        
        # Leer archivo
        huff_bytes = await file.read()
        
        # Descomprimir
        decompressed_text, original_filename, metrics = CompressionService.decompress_file(huff_bytes)
        
        # Guardar sesión
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "decompressed_text": decompressed_text,
            "filename": original_filename,
            "metrics": metrics
        }
        
        # Preview del texto
        text_preview = decompressed_text[:500] if len(decompressed_text) > 500 else decompressed_text
        
        return DecompressResponseSchema(
            success=True,
            original_filename=original_filename,
            original_size=metrics.original_size,
            compressed_size=metrics.compressed_size,
            compression_ratio=metrics.compression_ratio,
            text_preview=text_preview
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """
    Obtiene información de una sesión.
    
    Args:
        session_id: ID de la sesión
        
    Returns:
        Datos de la sesión
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    session = sessions[session_id]
    
    return {
        "session_id": session_id,
        "filename": session.get("filename"),
        "metrics": {
            "original_size": session["metrics"].original_size,
            "compressed_size": session["metrics"].compressed_size,
            "compression_ratio": session["metrics"].compression_ratio,
            "shannon_entropy": session["metrics"].shannon_entropy,
            "average_code_length": session["metrics"].average_code_length,
            "efficiency": session["metrics"].efficiency,
            "unique_characters": session["metrics"].unique_characters,
            "characters_count": session["metrics"].characters_count,
        },
        "visualization": session.get("visualization", {})
    }


@router.get("/download/{session_id}")
async def download_compressed(session_id: str):
    """
    Descarga el archivo comprimido.
    
    Args:
        session_id: ID de la sesión
        
    Returns:
        Archivo .huff
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    session = sessions[session_id]
    
    if "huff_bytes" not in session:
        raise HTTPException(status_code=400, detail="No hay archivo comprimido en esta sesión")
    
    # Crear archivo temporal
    temp_filename = f"{session_id}.huff"
    temp_path = f"/tmp/{temp_filename}"
    
    with open(temp_path, "wb") as f:
        f.write(session["huff_bytes"])
    
    return FileResponse(
        path=temp_path,
        filename=f"{session['filename'].replace('.txt', '')}.huff",
        media_type="application/octet-stream"
    )


@router.get("/download-text/{session_id}")
async def download_decompressed(session_id: str):
    """
    Descarga el archivo descomprimido.
    
    Args:
        session_id: ID de la sesión
        
    Returns:
        Archivo .txt original
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    session = sessions[session_id]
    
    if "decompressed_text" not in session:
        raise HTTPException(status_code=400, detail="No hay texto descomprimido en esta sesión")
    
    # Crear archivo temporal
    temp_filename = f"{session_id}.txt"
    temp_path = f"/tmp/{temp_filename}"
    
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(session["decompressed_text"])
    
    return FileResponse(
        path=temp_path,
        filename=session["filename"],
        media_type="text/plain"
    )


@router.get("/visualization/{session_id}")
async def get_visualization(session_id: str):
    """
    Obtiene datos de visualización (frecuencias, códigos, etc).
    
    Args:
        session_id: ID de la sesión
        
    Returns:
        Datos estructurados para visualización
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    session = sessions[session_id]
    visualization = session.get("visualization", {})
    
    return {
        "success": True,
        "data": visualization
    }
