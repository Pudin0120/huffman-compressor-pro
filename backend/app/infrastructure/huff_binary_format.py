"""
Infrastructure: Serialización y deserialización binaria
Manejo del formato .huff personalizado
"""

import struct
from io import BytesIO
from typing import Dict, Tuple
from app.domain.huffman_node import HuffmanNode


class HuffBinaryFormat:
    """
    Formato binario personalizado para archivos comprimidos .huff
    
    Estructura:
    ┌─ Magic Bytes (4 bytes): "HUFF"
    ├─ Version (1 byte): 0x01
    ├─ Original Filename Length (2 bytes): uint16
    ├─ Original Filename (variable)
    ├─ Original File Size (4 bytes): uint32
    ├─ Padding Bits (1 byte): uint8 (bits sin usar en el último byte)
    ├─ Frequencies Map Size (2 bytes): uint16
    ├─ Frequencies Map (variable): serializado como {char: frequency}
    └─ Compressed Data (variable): datos binarios comprimidos
    """
    
    MAGIC_BYTES = b"HUFF"
    VERSION = 0x01
    HEADER_MIN_SIZE = 14  # Magic(4) + Version(1) + Filename_len(2) + Size(4) + Padding(1) + Map_size(2)
    
    @staticmethod
    def bits_to_bytes(bit_string: str) -> bytes:
        """
        Convierte un string de bits a bytes.
        
        Ejemplo: "11010110" -> b'\xD6'
        
        Args:
            bit_string: String de bits (e.g., "01010110...")
            
        Returns:
            Bytes comprimidos
        """
        # Calcular padding necesario
        padding = (8 - (len(bit_string) % 8)) % 8
        bit_string = bit_string + "0" * padding
        
        byte_array = bytearray()
        for i in range(0, len(bit_string), 8):
            byte = int(bit_string[i:i+8], 2)
            byte_array.append(byte)
        
        return bytes(byte_array), padding
    
    @staticmethod
    def bytes_to_bits(data: bytes, padding: int) -> str:
        """
        Convierte bytes a string de bits.
        
        Ejemplo: b'\xD6' -> "11010110"
        
        Args:
            data: Bytes a convertir
            padding: Cantidad de bits de padding a remover del final
            
        Returns:
            String de bits
        """
        bit_string = "".join(format(byte, "08b") for byte in data)
        
        # Remover padding
        if padding > 0:
            bit_string = bit_string[:-padding]
        
        return bit_string
    
    @staticmethod
    def serialize_frequencies(frequencies: Dict[str, int]) -> bytes:
        """
        Serializa un diccionario de frecuencias a bytes.
        
        Formato:
        - Número de caracteres (2 bytes)
        - Para cada carácter:
          - Byte del carácter (1 byte)
          - Frecuencia (4 bytes, little-endian)
        
        Args:
            frequencies: Diccionario {char: frecuencia}
            
        Returns:
            Datos serializados
        """
        buffer = BytesIO()
        
        # Número de caracteres únicos
        buffer.write(struct.pack("<H", len(frequencies)))
        
        # Cada carácter y su frecuencia
        for char, freq in frequencies.items():
            # Usar UTF-8 para soportar caracteres especiales
            char_bytes = char.encode("utf-8")
            buffer.write(struct.pack("<H", len(char_bytes)))
            buffer.write(char_bytes)
            buffer.write(struct.pack("<I", freq))
        
        return buffer.getvalue()
    
    @staticmethod
    def deserialize_frequencies(data: bytes, offset: int = 0) -> Tuple[Dict[str, int], int]:
        """
        Deserializa frecuencias desde bytes.
        
        Args:
            data: Bytes a deserializar
            offset: Posición inicial en los datos
            
        Returns:
            Tupla (diccionario de frecuencias, nueva posición)
        """
        buffer = BytesIO(data)
        buffer.seek(offset)
        
        # Leer número de caracteres
        num_chars = struct.unpack("<H", buffer.read(2))[0]
        frequencies = {}
        
        for _ in range(num_chars):
            # Leer longitud del carácter
            char_len = struct.unpack("<H", buffer.read(2))[0]
            # Leer carácter
            char = buffer.read(char_len).decode("utf-8")
            # Leer frecuencia
            freq = struct.unpack("<I", buffer.read(4))[0]
            
            frequencies[char] = freq
        
        return frequencies, buffer.tell()
    
    @staticmethod
    def create_huff_file(
        original_filename: str,
        compressed_bits: str,
        frequencies: Dict[str, int]
    ) -> bytes:
        """
        Crea un archivo .huff completo con estructura binaria.
        
        Args:
            original_filename: Nombre del archivo original
            compressed_bits: String de bits comprimidos
            frequencies: Diccionario de frecuencias
            
        Returns:
            Bytes del archivo .huff
        """
        huff_file = BytesIO()
        
        # 1. Magic bytes
        huff_file.write(HuffBinaryFormat.MAGIC_BYTES)
        
        # 2. Version
        huff_file.write(struct.pack("B", HuffBinaryFormat.VERSION))
        
        # 3. Nombre del archivo original
        filename_bytes = original_filename.encode("utf-8")
        huff_file.write(struct.pack("<H", len(filename_bytes)))
        huff_file.write(filename_bytes)
        
        # 4. Tamaño original del archivo (en caracteres)
        original_size = sum(frequencies.values())
        huff_file.write(struct.pack("<I", original_size))
        
        # 5. Convertir bits a bytes y obtener padding
        compressed_bytes, padding = HuffBinaryFormat.bits_to_bytes(compressed_bits)
        huff_file.write(struct.pack("B", padding))
        
        # 6. Serializar frecuencias
        serialized_frequencies = HuffBinaryFormat.serialize_frequencies(frequencies)
        huff_file.write(serialized_frequencies)
        
        # 7. Datos comprimidos
        huff_file.write(compressed_bytes)
        
        return huff_file.getvalue()
    
    @staticmethod
    def read_huff_file(huff_data: bytes) -> Tuple[str, str, Dict[str, int], int]:
        """
        Lee y extrae la información de un archivo .huff.
        
        Args:
            huff_data: Bytes del archivo .huff
            
        Returns:
            Tupla (nombre_original, bits_comprimidos, frecuencias, tamaño_original)
        """
        buffer = BytesIO(huff_data)
        
        # 1. Verificar magic bytes
        magic = buffer.read(4)
        if magic != HuffBinaryFormat.MAGIC_BYTES:
            raise ValueError("Archivo .huff inválido: magic bytes incorrectos")
        
        # 2. Verificar versión
        version = struct.unpack("B", buffer.read(1))[0]
        if version != HuffBinaryFormat.VERSION:
            raise ValueError(f"Versión del archivo no soportada: {version}")
        
        # 3. Leer nombre del archivo original
        filename_len = struct.unpack("<H", buffer.read(2))[0]
        original_filename = buffer.read(filename_len).decode("utf-8")
        
        # 4. Leer tamaño original
        original_size = struct.unpack("<I", buffer.read(4))[0]
        
        # 5. Leer padding
        padding = struct.unpack("B", buffer.read(1))[0]
        
        # 6. Deserializar frecuencias
        remaining_data = buffer.read()
        frequencies, freq_offset = HuffBinaryFormat.deserialize_frequencies(remaining_data, 0)
        
        # 7. Leer datos comprimidos
        compressed_bytes = remaining_data[freq_offset:]
        compressed_bits = HuffBinaryFormat.bytes_to_bits(compressed_bytes, padding)
        
        return original_filename, compressed_bits, frequencies, original_size
