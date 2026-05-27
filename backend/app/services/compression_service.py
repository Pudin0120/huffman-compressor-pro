"""
Services: Casos de uso de compresión y descompresión
Orquesta el dominio y la infraestructura
"""

import time
from typing import Dict, Tuple, Optional
from app.core.huffman_algorithm import HuffmanAlgorithm
from app.infrastructure.huff_binary_format import HuffBinaryFormat
from app.domain.huffman_node import HuffmanCode, CompressionMetrics


class CompressionService:
    """Servicio de compresión"""
    
    @staticmethod
    def compress_text(text: str, filename: str = "file.txt") -> Tuple[bytes, CompressionMetrics, Dict]:
        """
        Comprime un texto usando el algoritmo de Huffman.
        
        Args:
            text: Texto a comprimir
            filename: Nombre del archivo original
            
        Returns:
            Tupla (datos_comprimidos, métricas, datos_para_visualización)
        """
        start_time = time.time()
        
        # Caso especial: texto vacío
        if not text:
            empty_metrics = CompressionMetrics(
                original_size=0,
                compressed_size=0,
                characters_count=0,
                unique_characters=0,
                shannon_entropy=0.0,
                average_code_length=0.0,
                compression_ratio=0.0,
                theoretical_minimum=0.0,
                efficiency=0.0,
                compression_time=0.0
            )
            return b"", empty_metrics, {}
        
        # 1. Contar frecuencias
        frequencies = HuffmanAlgorithm.count_frequencies(text)
        
        # 2. Construir árbol de Huffman
        root = HuffmanAlgorithm.build_huffman_tree(frequencies)
        
        # 3. Generar códigos
        codes = HuffmanAlgorithm.generate_codes(root)
        
        # 4. Codificar el texto
        encoded_bits = HuffmanAlgorithm.encode(text, codes)
        
        # 5. Crear archivo .huff
        huff_bytes = HuffBinaryFormat.create_huff_file(filename, encoded_bits, frequencies)
        
        # 6. Calcular métricas
        original_size = len(text.encode("utf-8"))  # Tamaño en UTF-8
        compressed_size = len(huff_bytes)
        
        shannon_entropy = HuffmanAlgorithm.calculate_shannon_entropy(text)
        average_code_length = HuffmanAlgorithm.calculate_average_code_length(codes, frequencies)
        compression_ratio = HuffmanAlgorithm.calculate_compression_ratio(original_size, compressed_size)
        efficiency = HuffmanAlgorithm.calculate_efficiency(average_code_length, shannon_entropy)
        
        compression_time = time.time() - start_time
        
        metrics = CompressionMetrics(
            original_size=original_size,
            compressed_size=compressed_size,
            characters_count=len(text),
            unique_characters=len(frequencies),
            shannon_entropy=shannon_entropy,
            average_code_length=average_code_length,
            compression_ratio=compression_ratio,
            theoretical_minimum=shannon_entropy,
            efficiency=efficiency,
            compression_time=compression_time
        )
        
        # 7. Preparar datos para visualización
        visualization_data = CompressionService._prepare_visualization_data(
            root, codes, frequencies, text
        )
        
        return huff_bytes, metrics, visualization_data
    
    @staticmethod
    def decompress_file(huff_bytes: bytes) -> Tuple[str, str, CompressionMetrics]:
        """
        Descomprime un archivo .huff.
        
        Args:
            huff_bytes: Datos del archivo .huff
            
        Returns:
            Tupla (texto_descomprimido, nombre_original, métricas)
        """
        # 1. Leer archivo .huff
        original_filename, compressed_bits, frequencies, original_size = HuffBinaryFormat.read_huff_file(huff_bytes)
        
        # 2. Reconstruir árbol de Huffman
        root = HuffmanAlgorithm.build_huffman_tree(frequencies)
        
        # 3. Decodificar
        decompressed_text = HuffmanAlgorithm.decode(compressed_bits, root)
        
        # 4. Crear métricas
        compressed_size = len(huff_bytes)
        shannon_entropy = HuffmanAlgorithm.calculate_shannon_entropy(decompressed_text)
        
        codes = HuffmanAlgorithm.generate_codes(root)
        average_code_length = HuffmanAlgorithm.calculate_average_code_length(codes, frequencies)
        
        compression_ratio = HuffmanAlgorithm.calculate_compression_ratio(original_size, compressed_size)
        efficiency = HuffmanAlgorithm.calculate_efficiency(average_code_length, shannon_entropy)
        
        metrics = CompressionMetrics(
            original_size=original_size,
            compressed_size=compressed_size,
            characters_count=len(decompressed_text),
            unique_characters=len(frequencies),
            shannon_entropy=shannon_entropy,
            average_code_length=average_code_length,
            compression_ratio=compression_ratio,
            theoretical_minimum=shannon_entropy,
            efficiency=efficiency,
            compression_time=0.0
        )
        
        return decompressed_text, original_filename, metrics
    
    @staticmethod
    def _prepare_visualization_data(root, codes: Dict[str, str], frequencies: Dict[str, int], text: str) -> Dict:
        """
        Prepara datos para visualización del árbol y análisis.
        
        Returns:
            Diccionario con datos estructurados para el frontend
        """
        # Tabla de frecuencias
        frequency_table = [
            {
                "char": char,
                "displayChar": repr(char) if char in ["\n", "\t", " "] else char,
                "frequency": freq,
                "percentage": (freq / len(text) * 100) if text else 0
            }
            for char, freq in sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        ]
        
        # Tabla de códigos
        code_table = [
            {
                "char": char,
                "displayChar": repr(char) if char in ["\n", "\t", " "] else char,
                "code": codes[char],
                "bits": len(codes[char]),
                "frequency": frequencies[char],
                "size_in_bits": len(codes[char]) * frequencies[char]
            }
            for char in sorted(codes.keys())
        ]
        
        # Datos para visualización del árbol (será mejorado)
        tree_data = {
            "frequencies": frequency_table,
            "codes": code_table,
            "total_chars": len(text),
            "unique_chars": len(frequencies),
            "compressed_bits": sum(len(code) * freq for code, freq in zip(codes.values(), frequencies.values()))
        }
        
        return tree_data
