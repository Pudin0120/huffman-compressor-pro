"""
Pruebas unitarias del algoritmo de Huffman
"""

import pytest
from app.core.huffman_algorithm import HuffmanAlgorithm
from app.infrastructure.huff_binary_format import HuffBinaryFormat
from app.services.compression_service import CompressionService


class TestHuffmanAlgorithm:
    """Tests para el algoritmo de Huffman"""
    
    def test_count_frequencies(self):
        """Prueba el conteo de frecuencias"""
        text = "hello world"
        freqs = HuffmanAlgorithm.count_frequencies(text)
        
        assert freqs["l"] == 3
        assert freqs["o"] == 2
        assert freqs["h"] == 1
        assert len(freqs) == 8  # h, e, l, o, , w, r, d
    
    def test_build_huffman_tree_simple(self):
        """Prueba construcción del árbol con texto simple"""
        frequencies = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
        root = HuffmanAlgorithm.build_huffman_tree(frequencies)
        
        assert root is not None
        assert root.frequency == 100
        assert not root.is_leaf()
    
    def test_build_huffman_tree_empty(self):
        """Prueba construcción con diccionario vacío"""
        root = HuffmanAlgorithm.build_huffman_tree({})
        assert root is None
    
    def test_build_huffman_tree_single_char(self):
        """Prueba construcción con un solo carácter"""
        frequencies = {"a": 5}
        root = HuffmanAlgorithm.build_huffman_tree(frequencies)
        
        assert root is not None
        assert root.frequency == 5
        # Con un solo carácter se crea un nodo raíz artificial
        assert root.left is not None
    
    def test_generate_codes_simple(self):
        """Prueba generación de códigos"""
        frequencies = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
        root = HuffmanAlgorithm.build_huffman_tree(frequencies)
        codes = HuffmanAlgorithm.generate_codes(root)
        
        assert len(codes) == 6
        # Los códigos deben ser strings de bits
        for char, code in codes.items():
            assert all(bit in "01" for bit in code)
    
    def test_prefix_free_codes(self):
        """Verifica que los códigos sean libres de prefijo"""
        frequencies = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
        root = HuffmanAlgorithm.build_huffman_tree(frequencies)
        codes = HuffmanAlgorithm.generate_codes(root)
        
        code_list = list(codes.values())
        for i, code1 in enumerate(code_list):
            for j, code2 in enumerate(code_list):
                if i != j:
                    assert not code1.startswith(code2)
                    assert not code2.startswith(code1)
    
    def test_encode_decode(self):
        """Prueba que codificación y decodificación sean inversas"""
        text = "hello world"
        frequencies = HuffmanAlgorithm.count_frequencies(text)
        root = HuffmanAlgorithm.build_huffman_tree(frequencies)
        codes = HuffmanAlgorithm.generate_codes(root)
        
        encoded = HuffmanAlgorithm.encode(text, codes)
        decoded = HuffmanAlgorithm.decode(encoded, root)
        
        assert decoded == text
    
    def test_shannon_entropy(self):
        """Prueba el cálculo de entropía de Shannon"""
        text = "hello world"
        entropy = HuffmanAlgorithm.calculate_shannon_entropy(text)
        
        # La entropía debe estar entre 0 y log2(unique_chars)
        assert 0 <= entropy <= HuffmanAlgorithm.calculate_shannon_entropy("abcdefghij")
    
    def test_average_code_length(self):
        """Prueba el cálculo de longitud promedio de código"""
        frequencies = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
        root = HuffmanAlgorithm.build_huffman_tree(frequencies)
        codes = HuffmanAlgorithm.generate_codes(root)
        
        avg_length = HuffmanAlgorithm.calculate_average_code_length(codes, frequencies)
        
        # La longitud promedio debe ser positiva
        assert avg_length > 0
    
    def test_compression_ratio(self):
        """Prueba el cálculo del ratio de compresión"""
        original = 1000
        compressed = 600
        ratio = HuffmanAlgorithm.calculate_compression_ratio(original, compressed)
        
        assert ratio == 40.0  # (1000 - 600) / 1000 * 100 = 40
    
    def test_efficiency(self):
        """Prueba el cálculo de eficiencia"""
        entropy = 4.5
        avg_length = 4.7
        efficiency = HuffmanAlgorithm.calculate_efficiency(avg_length, entropy)
        
        assert 0 <= efficiency <= 100


class TestBinaryFormat:
    """Tests para el formato binario .huff"""
    
    def test_bits_to_bytes_conversion(self):
        """Prueba conversión de bits a bytes"""
        bits = "11010110"
        byte_data, padding = HuffBinaryFormat.bits_to_bytes(bits)
        
        assert len(byte_data) == 1
        assert byte_data[0] == 0xD6  # 11010110 en hex
        assert padding == 0
    
    def test_bits_to_bytes_with_padding(self):
        """Prueba conversión con padding"""
        bits = "1101011"  # 7 bits, necesita 1 bit de padding
        byte_data, padding = HuffBinaryFormat.bits_to_bytes(bits)
        
        assert len(byte_data) == 1
        assert padding == 1
    
    def test_bytes_to_bits_conversion(self):
        """Prueba conversión inversa de bytes a bits"""
        original_bits = "11010110"
        byte_data, padding = HuffBinaryFormat.bits_to_bytes(original_bits)
        restored_bits = HuffBinaryFormat.bytes_to_bits(byte_data, padding)
        
        assert restored_bits == original_bits
    
    def test_serialize_deserialize_frequencies(self):
        """Prueba serialización de frecuencias"""
        frequencies = {"a": 100, "b": 50, "c": 25}
        serialized = HuffBinaryFormat.serialize_frequencies(frequencies)
        
        deserialized, _ = HuffBinaryFormat.deserialize_frequencies(serialized)
        
        assert deserialized == frequencies
    
    def test_huff_file_roundtrip(self):
        """Prueba creación y lectura de archivo .huff"""
        original_filename = "test.txt"
        compressed_bits = "110101101110"
        frequencies = {"a": 100, "b": 50, "c": 25}
        
        # Crear archivo
        huff_data = HuffBinaryFormat.create_huff_file(original_filename, compressed_bits, frequencies)
        
        # Leer archivo
        filename, bits, freqs, size = HuffBinaryFormat.read_huff_file(huff_data)
        
        assert filename == original_filename
        assert bits == compressed_bits
        assert freqs == frequencies
        assert size == 175  # 100 + 50 + 25


class TestCompressionService:
    """Tests para el servicio de compresión"""
    
    def test_compress_decompress_roundtrip(self):
        """Prueba compresión y descompresión completa"""
        text = "The quick brown fox jumps over the lazy dog"
        filename = "test.txt"
        
        # Comprimir
        huff_bytes, metrics, viz = CompressionService.compress_text(text, filename)
        
        assert huff_bytes is not None
        assert metrics.original_size > 0
        assert metrics.compressed_size > 0
        
        # Descomprimir
        decompressed, orig_filename, metrics2 = CompressionService.decompress_file(huff_bytes)
        
        assert decompressed == text
        assert orig_filename == filename
    
    def test_compress_empty_text(self):
        """Prueba compresión de texto vacío"""
        huff_bytes, metrics, viz = CompressionService.compress_text("", "empty.txt")
        
        assert huff_bytes == b""
        assert metrics.original_size == 0
    
    def test_compress_single_character(self):
        """Prueba compresión de un solo carácter repetido"""
        text = "aaaaaaaaaa"
        huff_bytes, metrics, viz = CompressionService.compress_text(text, "single.txt")
        
        assert huff_bytes is not None
        assert metrics.compression_ratio >= 0
        
        # Descomprimir
        decompressed, _, _ = CompressionService.decompress_file(huff_bytes)
        assert decompressed == text
    
    def test_compress_unicode(self):
        """Prueba compresión de caracteres Unicode"""
        text = "Hola mundo 🌍 ñ ü é"
        huff_bytes, metrics, viz = CompressionService.compress_text(text, "unicode.txt")
        
        # Descomprimir
        decompressed, _, _ = CompressionService.decompress_file(huff_bytes)
        assert decompressed == text
    
    def test_metrics_coherence(self):
        """Verifica que las métricas sean coherentes"""
        text = "hello world hello"
        huff_bytes, metrics, viz = CompressionService.compress_text(text, "test.txt")
        
        # La longitud media debe ser mayor o igual a la entropía
        assert metrics.average_code_length >= metrics.shannon_entropy
        
        # La eficiencia debe estar entre 0 y 100
        assert 0 <= metrics.efficiency <= 100
        
        # El ratio debe estar entre -100 y 100
        assert -100 <= metrics.compression_ratio <= 100
