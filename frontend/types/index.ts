"""
Tipos de TypeScript compartidos
"""

export interface CompressionMetrics {
  original_size: number;
  compressed_size: number;
  compression_ratio: number;
  shannon_entropy: number;
  average_code_length: number;
  efficiency: number;
  unique_characters: number;
  characters_count: number;
  compression_time?: number;
}

export interface FrequencyItem {
  char: string;
  displayChar: string;
  frequency: number;
  percentage: number;
}

export interface CodeItem {
  char: string;
  displayChar: string;
  code: string;
  bits: number;
  frequency: number;
  size_in_bits: number;
}

export interface VisualizationData {
  frequencies: FrequencyItem[];
  codes: CodeItem[];
  total_chars: number;
  unique_chars: number;
  compressed_bits: number;
}

export interface CompressResponse {
  success: boolean;
  session_id: string;
  original_size: number;
  compressed_size: number;
  compression_ratio: number;
  shannon_entropy: number;
  average_code_length: number;
  efficiency: number;
  unique_characters: number;
  characters_count: number;
  compression_time?: number;
}

export interface DecompressResponse {
  success: boolean;
  original_filename: string;
  original_size: number;
  compressed_size: number;
  compression_ratio: number;
  text_preview: string;
}

export interface Session {
  session_id: string;
  filename: string;
  metrics: CompressionMetrics;
  visualization: VisualizationData;
}
