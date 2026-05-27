"""
Core: Algoritmo de Huffman puro
Implementación correcta del algoritmo, independiente de la presentación
"""

import heapq
import math
from typing import Dict, Tuple, List, Optional
from collections import Counter
from app.domain.huffman_node import HuffmanNode, HuffmanCode


class HuffmanAlgorithm:
    """
    Implementación completa y correcta del algoritmo de Huffman.
    
    Garantiza:
    - Códigos libres de prefijo
    - Compresión óptima (greedy)
    - Complejidad O(n log n) en construcción del árbol
    - Manejo de edge cases
    """
    
    @staticmethod
    def count_frequencies(text: str) -> Dict[str, int]:
        """
        Cuenta la frecuencia de cada carácter en el texto.
        
        Args:
            text: Texto de entrada
            
        Returns:
            Diccionario {carácter: frecuencia}
        """
        return dict(Counter(text))
    
    @staticmethod
    def build_huffman_tree(frequencies: Dict[str, int]) -> Optional[HuffmanNode]:
        """
        Construye el árbol de Huffman usando un min-heap.
        
        Complejidad: O(n log n) donde n es el número de símbolos únicos.
        
        Args:
            frequencies: Diccionario de frecuencias
            
        Returns:
            Raíz del árbol de Huffman o None si está vacío
            
        Edge cases:
            - Texto vacío: retorna None
            - Un solo carácter: retorna nodo hoja con altura especial
        """
        if not frequencies:
            return None
        
        # Crear nodos hoja para cada carácter
        heap: List[Tuple[int, int, HuffmanNode]] = []
        counter = 0
        
        for char, freq in frequencies.items():
            node = HuffmanNode(frequency=freq, char=char)
            heapq.heappush(heap, (freq, counter, node))
            counter += 1
        
        # Si solo hay un carácter, crear un nodo raíz artificial
        if len(heap) == 1:
            _, _, node = heapq.heappop(heap)
            root = HuffmanNode(frequency=node.frequency, left=node)
            return root
        
        # Construir el árbol combinando los dos nodos mínimos repetidamente
        while len(heap) > 1:
            freq1, _, left_node = heapq.heappop(heap)
            freq2, _, right_node = heapq.heappop(heap)
            
            parent_freq = freq1 + freq2
            parent = HuffmanNode(frequency=parent_freq, left=left_node, right=right_node)
            
            heapq.heappush(heap, (parent_freq, counter, parent))
            counter += 1
        
        _, _, root = heapq.heappop(heap)
        return root
    
    @staticmethod
    def generate_codes(node: Optional[HuffmanNode], prefix: str = "") -> Dict[str, str]:
        """
        Genera recursivamente los códigos Huffman desde el árbol.
        
        Args:
            node: Nodo actual del árbol
            prefix: Código acumulado hasta aquí
            
        Returns:
            Diccionario {carácter: código}
        """
        if node is None:
            return {}
        
        codes = {}
        
        # Caso base: es una hoja
        if node.is_leaf():
            # Si el árbol tiene solo una hoja, asignar código "0"
            codes[node.char] = prefix if prefix else "0"
            return codes
        
        # Caso recursivo: recorrer izquierda con "0" y derecha con "1"
        if node.left:
            codes.update(HuffmanAlgorithm.generate_codes(node.left, prefix + "0"))
        
        if node.right:
            codes.update(HuffmanAlgorithm.generate_codes(node.right, prefix + "1"))
        
        return codes
    
    @staticmethod
    def encode(text: str, codes: Dict[str, str]) -> str:
        """
        Codifica el texto usando los códigos Huffman.
        
        Args:
            text: Texto a codificar
            codes: Diccionario de códigos {char: código_binario}
            
        Returns:
            String de bits (e.g., "01010110...")
        """
        return "".join(codes[char] for char in text)
    
    @staticmethod
    def decode(encoded_bits: str, root: Optional[HuffmanNode]) -> str:
        """
        Decodifica un string de bits usando el árbol de Huffman.
        
        Args:
            encoded_bits: String de bits a decodificar
            root: Raíz del árbol de Huffman
            
        Returns:
            Texto decodificado
        """
        if root is None or not encoded_bits:
            return ""
        
        # Caso especial: árbol con un solo carácter
        if root.is_leaf():
            return root.char * len(encoded_bits)
        
        decoded = []
        current = root
        
        for bit in encoded_bits:
            # Navegar por el árbol: 0 = izquierda, 1 = derecha
            if bit == "0":
                current = current.left
            else:
                current = current.right
            
            # Si llegamos a una hoja, registrar el carácter
            if current.is_leaf():
                decoded.append(current.char)
                current = root
        
        return "".join(decoded)
    
    @staticmethod
    def calculate_shannon_entropy(text: str) -> float:
        """
        Calcula la entropía de Shannon del texto.
        
        H(X) = -Σ P(x) * log2(P(x))
        
        La entropía representa el número mínimo teórico de bits por símbolo.
        
        Args:
            text: Texto de entrada
            
        Returns:
            Entropía en bits por símbolo
        """
        if not text:
            return 0.0
        
        frequencies = Counter(text)
        text_length = len(text)
        entropy = 0.0
        
        for freq in frequencies.values():
            probability = freq / text_length
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    @staticmethod
    def calculate_average_code_length(codes: Dict[str, str], frequencies: Dict[str, int]) -> float:
        """
        Calcula la longitud media de los códigos Huffman.
        
        L_avg = Σ P(x) * |código(x)|
        
        Args:
            codes: Diccionario de códigos
            frequencies: Diccionario de frecuencias
            
        Returns:
            Longitud promedio en bits por símbolo
        """
        if not codes or not frequencies:
            return 0.0
        
        total_symbols = sum(frequencies.values())
        average_length = 0.0
        
        for char, code in codes.items():
            frequency = frequencies.get(char, 0)
            average_length += (frequency / total_symbols) * len(code)
        
        return average_length
    
    @staticmethod
    def calculate_compression_ratio(original_size: int, compressed_size: int) -> float:
        """
        Calcula el ratio de compresión.
        
        Ratio = (original - compressed) / original * 100
        
        Args:
            original_size: Tamaño original en bytes
            compressed_size: Tamaño comprimido en bytes
            
        Returns:
            Porcentaje de reducción (0-100)
        """
        if original_size == 0:
            return 0.0
        
        return max(0.0, ((original_size - compressed_size) / original_size) * 100)
    
    @staticmethod
    def calculate_efficiency(average_code_length: float, shannon_entropy: float) -> float:
        """
        Calcula la eficiencia teórica de la compresión.
        
        Eficiencia = Entropía / Longitud Media * 100
        
        Una eficiencia del 100% significa que estamos en el límite teórico óptimo.
        
        Args:
            average_code_length: Longitud promedio del código
            shannon_entropy: Entropía de Shannon
            
        Returns:
            Porcentaje de eficiencia (0-100)
        """
        if shannon_entropy == 0.0 or average_code_length == 0.0:
            return 0.0
        
        efficiency = (shannon_entropy / average_code_length) * 100
        return min(efficiency, 100.0)  # Capped a 100%
