"""
Schemas: Modelos de validación con Pydantic
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class CompressResponseSchema(BaseModel):
    """Respuesta de compresión"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "session_id": "abc123",
                "original_size": 1024,
                "compressed_size": 512,
                "compression_ratio": 50.0,
                "shannon_entropy": 4.5,
                "average_code_length": 4.6,
                "efficiency": 97.8,
                "unique_characters": 26,
                "characters_count": 1000
            }
        }
    
    success: bool
    session_id: str
    original_size: int
    compressed_size: int
    compression_ratio: float
    shannon_entropy: float
    average_code_length: float
    efficiency: float
    unique_characters: int
    characters_count: int
    compression_time: Optional[float] = None


class DecompressResponseSchema(BaseModel):
    """Respuesta de descompresión"""
    
    success: bool
    session_id: str
    original_filename: str
    original_size: int
    compressed_size: int
    compression_ratio: float
    text_preview: str = Field(..., description="Primeros 500 caracteres del texto")


class FrequencyItemSchema(BaseModel):
    """Ítem de la tabla de frecuencias"""
    
    char: str
    displayChar: str
    frequency: int
    percentage: float


class CodeItemSchema(BaseModel):
    """Ítem de la tabla de códigos"""
    
    char: str
    displayChar: str
    code: str
    bits: int
    frequency: int
    size_in_bits: int


class VisualizationDataSchema(BaseModel):
    """Datos para visualización"""
    
    frequencies: List[FrequencyItemSchema]
    codes: List[CodeItemSchema]
    total_chars: int
    unique_chars: int
    compressed_bits: int


class MetricsResponseSchema(BaseModel):
    """Métricas completas"""
    
    shannon_entropy: float
    average_code_length: float
    compression_ratio: float
    efficiency: float
    theoretical_minimum: float


class TreeNodeSchema(BaseModel):
    """Nodo del árbol para visualización"""
    
    id: str
    value: Optional[int] = None
    char: Optional[str] = None
    children: List['TreeNodeSchema'] = []


class TreeResponseSchema(BaseModel):
    """Respuesta con árbol visualizable"""
    
    root: TreeNodeSchema
    nodes_count: int
    tree_height: int


TreeNodeSchema.model_rebuild()


class ErrorResponseSchema(BaseModel):
    """Respuesta de error"""
    
    success: bool = False
    error: str
    error_code: Optional[str] = None
    details: Optional[Dict] = None
