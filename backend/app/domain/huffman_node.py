"""
Domain: Nodos del árbol de Huffman
Entidades core del problema de compresión
"""

from dataclasses import dataclass
from typing import Optional, Any


@dataclass(order=True)
class HuffmanNode:
    """
    Nodo del árbol de Huffman.
    
    Comparable por frecuencia para usarlo en el heap mínimo.
    Attributes:
        frequency: Frecuencia del símbolo o suma de frecuencias
        char: Carácter representado (None para nodos internos)
        left: Hijo izquierdo
        right: Hijo derecho
        id: Identificador único para visualización
    """
    
    frequency: int
    char: Optional[str] = None
    left: Optional['HuffmanNode'] = None
    right: Optional['HuffmanNode'] = None
    id: Optional[str] = None
    
    def __post_init__(self):
        """Generar ID único basado en el contenido"""
        if self.id is None:
            if self.char:
                self.id = f"leaf_{ord(self.char)}_{self.frequency}"
            else:
                self.id = f"internal_{id(self)}_{self.frequency}"
    
    def is_leaf(self) -> bool:
        """Determina si este es un nodo hoja"""
        return self.char is not None
    
    def get_height(self) -> int:
        """Calcula la altura del árbol desde este nodo"""
        if self.is_leaf():
            return 0
        
        left_height = self.left.get_height() if self.left else 0
        right_height = self.right.get_height() if self.right else 0
        
        return 1 + max(left_height, right_height)
    
    def get_total_nodes(self) -> int:
        """Cuenta el total de nodos en el árbol desde aquí"""
        if self.is_leaf():
            return 1
        
        total = 1
        if self.left:
            total += self.left.get_total_nodes()
        if self.right:
            total += self.right.get_total_nodes()
        
        return total


@dataclass
class HuffmanCode:
    """Código Huffman asignado a un carácter"""
    char: str
    code: str
    frequency: int
    bits: int
    
    def __repr__(self) -> str:
        return f"'{self.char}' -> {self.code} (freq={self.frequency}, bits={self.bits})"


@dataclass
class CompressionMetrics:
    """Métricas de una compresión"""
    original_size: int
    compressed_size: int
    characters_count: int
    unique_characters: int
    shannon_entropy: float
    average_code_length: float
    compression_ratio: float
    theoretical_minimum: float
    efficiency: float
    compression_time: float
