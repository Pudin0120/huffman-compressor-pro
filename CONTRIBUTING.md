# Guía de Contribución - Huffman Compressor Pro

¡Gracias por tu interés en contribuir a Huffman Compressor Pro! Este documento proporciona pautas para contribuir al proyecto.

## Cómo Contribuir

### 1. Reportar Bugs

Si encuentras un bug, crea un issue en GitHub:

**Título**: Breve descripción del bug
**Descripción**: 
- Describe el comportamiento esperado
- Describe el comportamiento actual
- Pasos para reproducir
- Sistema operativo y versión
- Navegador (para frontend)

```markdown
### Descripción
El archivo .huff no se descarga correctamente

### Pasos para Reproducir
1. Subir archivo de 500KB
2. Comprimir
3. Hacer clic en "Descargar comprimido"

### Error
Descarga incompleta, archivo corrupto

### Sistema
- OS: Linux Ubuntu 22.04
- Browser: Chrome 120
- Backend: v1.0.0
```

### 2. Sugerir Mejoras

Abre un issue con la etiqueta `enhancement`:

```markdown
### Descripción
Agregar soporte para ZIP además de Huffman

### Beneficio
Permitiría comprimir múltiples archivos

### Alternativas Consideradas
- Crear nuevo proyecto separado
- Agregarlo a esta aplicación
```

### 3. Enviar Pull Requests

#### Prerequisitos
- Fork el repositorio
- Crear rama desde `main`: `git checkout -b feature/nombre`
- Hacer commits descriptivos
- Escribir tests para nuevas features
- Actualizar documentación

#### Proceso

1. **Fork & Clone**
```bash
git clone https://github.com/tu-usuario/huffman-compressor-pro.git
cd huffman-compressor-pro
git remote add upstream https://github.com/usuario-original/huffman-compressor-pro.git
```

2. **Crear Rama**
```bash
git checkout -b feature/tu-feature
# o para bugfix
git checkout -b fix/nombre-del-bug
```

3. **Hacer Cambios**
- Seguir el estilo de código existente
- Escribir tests
- Actualizar documentación

4. **Commit**
```bash
git add .
git commit -m "feat: descripción clara de la feature"
# o
git commit -m "fix: descripción del bug"
```

5. **Push a tu Fork**
```bash
git push origin feature/tu-feature
```

6. **Crear Pull Request**
- Ir a GitHub
- Comparar ramas
- Llenar template de PR
- Esperar revisión

### Convenciones de Commits

```
feat: agregar nueva feature
fix: corregir bug
docs: actualizar documentación
style: cambios de formato (no afectan lógica)
refactor: reorganizar código
perf: mejorar rendimiento
test: agregar o actualizar tests
chore: actualizar dependencias, etc
```

Ejemplos:
```bash
git commit -m "feat: agregar visualización interactiva del árbol"
git commit -m "fix: corregir desbordamiento de memoria en archivos grandes"
git commit -m "docs: actualizar README con nuevos endpoints"
git commit -m "test: agregar tests para descompresión Unicode"
```

## Estándares de Código

### Backend (Python)

**Estilo**: PEP 8
```bash
# Verificar con Black
pip install black
black .

# Verificar con Flake8
pip install flake8
flake8 .
```

```python
# Buen ejemplo
def compress_text(text: str, filename: str = "file.txt") -> Tuple[bytes, CompressionMetrics]:
    """
    Comprime un texto usando Huffman.
    
    Args:
        text: Texto a comprimir
        filename: Nombre del archivo
        
    Returns:
        Tupla (datos comprimidos, métricas)
    """
    if not text:
        raise ValueError("Texto no puede estar vacío")
    
    frequencies = HuffmanAlgorithm.count_frequencies(text)
    root = HuffmanAlgorithm.build_huffman_tree(frequencies)
    
    return huff_bytes, metrics
```

**Requisitos**:
- Type hints en todas las funciones
- Docstrings en formato Google/NumPy
- Máximo 88 caracteres por línea (Black)
- Tests para nuevas funciones

### Frontend (TypeScript/React)

**Estilo**: ESLint + Prettier
```bash
cd frontend
npm run lint
npm run format
```

```typescript
// Buen ejemplo
interface CompressionMetrics {
  original_size: number;
  compressed_size: number;
  compression_ratio: number;
}

export default function MetricsDisplay({ metrics }: { metrics: CompressionMetrics }) {
  return (
    <div className="space-y-4">
      {/* Contenido */}
    </div>
  );
}
```

**Requisitos**:
- Types completos en interfaces
- Componentes funcionales con hooks
- Props documentadas
- Tests con Jest/React Testing Library
- Máximo 100 caracteres por línea

## Testing

### Backend

```bash
cd backend
source venv/bin/activate

# Ejecutar todos los tests
pytest tests/

# Con cobertura
pytest tests/ --cov=app

# Test específico
pytest tests/test_huffman.py::TestHuffmanAlgorithm::test_encode_decode

# Verbose
pytest -v
```

### Frontend

```bash
cd frontend

# Tests
npm test

# Coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

**Cobertura Mínima**: 80% de coverage

## Documentación

### README
- Mantener actualizado con nuevas features
- Agregar ejemplos de uso
- Actualizar tabla de contenidos

### Docstrings
```python
def function_name(param1: str) -> int:
    """
    Breve descripción.
    
    Descripción más larga si es necesaria.
    
    Args:
        param1: Descripción del parámetro
        
    Returns:
        Descripción del retorno
        
    Raises:
        ValueError: Cuándo se lanza
        
    Example:
        >>> result = function_name("input")
        >>> result
        42
    """
```

### Comments
```python
# Solo para lógica compleja
# Explicar el "por qué", no el "qué"

# ❌ Malo
x = x + 1  # Incrementar x

# ✅ Bueno
# Incrementar índice para el siguiente batch
x = x + 1
```

## Revisión de Código

### Para Autores de PRs
- Responder comentarios prontamente
- Hacer commits adicionales en lugar de squash (mientras se revisa)
- Ser receptivo a feedback
- Actualizar descripción del PR si cambian requisitos

### Para Revisores
- Ser respetuoso y constructivo
- Explicar el "por qué" de comentarios
- Sugerir mejoras, no demandas
- Aprobar cuando todo está correcto

## Areas para Contribuir

### Backend
- [ ] Agregar más algoritmos de compresión
- [ ] Implementar base de datos para historial
- [ ] Cache con Redis
- [ ] Autenticación con JWT
- [ ] Soporte para múltiples archivos
- [ ] Estadísticas de uso

### Frontend
- [ ] Tema claro/oscuro toggle mejorado
- [ ] Historial de sesiones
- [ ] Compartir resultados
- [ ] Gráficos más avanzados
- [ ] Documentación interactiva
- [ ] Soporte offline

### Documentación
- [ ] Tutoriales en video
- [ ] Blog con casos de uso
- [ ] Traducción a otros idiomas
- [ ] Diagramas del algoritmo

### Infraestructura
- [ ] GitHub Actions CI/CD
- [ ] Kubernetes deployment
- [ ] Terraform para IaC
- [ ] Performance benchmarks

## Código de Conducta

### Esperamos
- ✅ Respeto entre contribuidores
- ✅ Comunicación clara y constructiva
- ✅ Reconocer contribuciones
- ✅ Ayuda a nuevos contribuidores

### No Toleramos
- ❌ Acoso o discriminación
- ❌ Lenguaje ofensivo
- ❌ Comportamiento inapropiado
- ❌ Spam

## Preguntas?

- 📖 Lee el [README.md](README.md)
- 📚 Consulta la [API Docs](DEPLOYMENT.md)
- 💬 Abre una [Discussion](https://github.com/usuario/huffman-compressor-pro/discussions)
- 📧 Contacta: tu-email@example.com

---

¡Gracias por contribuir! 🙏
