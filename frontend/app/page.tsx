'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Download, Copy, RotateCcw, Zap } from 'lucide-react'
import toast from 'react-hot-toast'
import FileUploadZone from '@/components/FileUploadZone'
import MetricsDisplay from '@/components/MetricsDisplay'
import { FrequencyTable, CodeTable } from '@/components/TablesDisplay'
import HuffmanTreeVisualizer from '@/components/HuffmanTreeVisualizer'
import { useCompressionStore } from '@/lib/store'
import { compressionApi } from '@/lib/api'

export default function Home() {
  const { currentSession, isCompressing, error, clearSession } = useCompressionStore()
  const [isInitializing, setIsInitializing] = useState(true)
  const [textInput, setTextInput] = useState('')
  const [showTextInput, setShowTextInput] = useState(false)

  useEffect(() => {
    const checkBackend = async () => {
      try {
        await compressionApi.healthCheck()
      } catch (error) {
        toast.error('No se pudo conectar con el servidor backend. Asegúrate de que esté ejecutándose.')
      } finally {
        setIsInitializing(false)
      }
    }
    checkBackend()
  }, [])

  const handleCompressText = async () => {
    if (!textInput.trim()) {
      toast.error('Por favor ingresa algún texto')
      return
    }

    try {
      const { setCurrentSession, setIsCompressing: setCompressing, setError: setErr } = useCompressionStore.getState()
      setCompressing(true)
      setErr(null)

      const response = await compressionApi.compressText(textInput)
      const session = await compressionApi.getSession(response.session_id)
      setCurrentSession(session)

      toast.success('Texto comprimido exitosamente')
      setShowTextInput(false)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error desconocido'
      toast.error(message)
    } finally {
      const { setIsCompressing: setCompressing } = useCompressionStore.getState()
      setCompressing(false)
    }
  }

  const handleDownloadCompressed = async () => {
    if (!currentSession?.session_id) return
    try {
      const blob = await compressionApi.downloadCompressed(currentSession.session_id)
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${currentSession.filename.replace('.txt', '')}.huff`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      toast.success('Archivo descargado exitosamente')
    } catch (err) {
      toast.error('Error al descargar el archivo')
    }
  }

  const handleDownloadDecompressed = async () => {
    if (!currentSession?.session_id) return
    try {
      const blob = await compressionApi.downloadDecompressed(currentSession.session_id)
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = currentSession.filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      toast.success('Archivo descargado exitosamente')
    } catch (err) {
      toast.error('Error al descargar el archivo')
    }
  }

  if (isInitializing) {
    return (
      <div className="min-h-screen bg-gradient-dark flex items-center justify-center">
        <motion.div animate={{ rotate: 360 }} transition={{ duration: 2, repeat: Infinity }}>
          <Zap className="w-12 h-12 text-primary" />
        </motion.div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-dark">
      {/* Header */}
      <header className="border-b border-border backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Zap className="w-8 h-8 text-primary" />
            <h1 className="text-2xl font-bold bg-gradient-to-r from-green-400 to-emerald-600 bg-clip-text text-transparent">
              Huffman Compressor Pro
            </h1>
          </div>
          <div className="text-xs text-muted-foreground">v1.0.0</div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
          {/* Hero Section */}
          {!currentSession && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center space-y-4 mb-8"
            >
              <h2 className="text-4xl font-bold text-foreground">Compresión Inteligente de Archivos</h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Utiliza el algoritmo de Huffman para comprimir y descomprimir archivos con una interfaz moderna y análisis detallado
              </p>
            </motion.div>
          )}

          {/* Área de carga o sesión actual */}
          {!currentSession ? (
            <div className="space-y-6">
              <FileUploadZone />

              {/* Opción de texto directo */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="border border-border rounded-xl p-6 bg-card/50"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-semibold text-foreground">O comprime texto directamente</h3>
                  <button
                    onClick={() => setShowTextInput(!showTextInput)}
                    className="text-sm px-3 py-1 rounded bg-primary/20 text-primary hover:bg-primary/30 transition-colors"
                  >
                    {showTextInput ? 'Cancelar' : 'Escribir texto'}
                  </button>
                </div>

                {showTextInput && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="space-y-4"
                  >
                    <textarea
                      value={textInput}
                      onChange={(e) => setTextInput(e.target.value)}
                      placeholder="Pega o escribe el texto que deseas comprimir..."
                      className="w-full h-48 p-4 bg-background border border-border rounded-lg text-foreground resize-none focus:outline-none focus:ring-2 focus:ring-primary"
                    />
                    <button
                      onClick={handleCompressText}
                      disabled={isCompressing || !textInput.trim()}
                      className="w-full px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed font-semibold transition-colors"
                    >
                      {isCompressing ? 'Comprimiendo...' : 'Comprimir Texto'}
                    </button>
                  </motion.div>
                )}
              </motion.div>
            </div>
          ) : (
            /* Mostrar resultados */
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              {/* Encabezado de sesión */}
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-foreground">{currentSession.filename}</h2>
                  <p className="text-sm text-muted-foreground mt-1">
                    Sesión procesada correctamente. Visualiza métricas y descarga resultados.
                  </p>
                </div>
                <button
                  onClick={clearSession}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-secondary text-secondary-foreground hover:bg-secondary/80 transition-colors"
                >
                  <RotateCcw className="w-4 h-4" />
                  Nueva compresión
                </button>
              </div>

              {/* Botones de descarga */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleDownloadCompressed}
                  className="flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 font-semibold transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Descargar Archivo Comprimido (.huff)
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleDownloadDecompressed}
                  className="flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-secondary text-secondary-foreground hover:bg-secondary/80 font-semibold transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Descargar Archivo Original (.txt)
                </motion.button>
              </div>

              {/* Métricas */}
              <div>
                <h3 className="text-xl font-bold text-foreground mb-4">Análisis de Compresión</h3>
                <MetricsDisplay metrics={currentSession.metrics} />
              </div>

              {/* Tablas y visualización */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <FrequencyTable frequencies={currentSession.visualization.frequencies} />
                </div>
                <div>
                  <HuffmanTreeVisualizer treeData={currentSession.visualization} />
                </div>
              </div>

              {/* Tabla de códigos */}
              <CodeTable codes={currentSession.visualization.codes} />

              {/* Información teórica */}
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="border border-border rounded-xl p-6 bg-card/50 space-y-4"
              >
                <h3 className="font-semibold text-foreground">Sobre esta compresión</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-muted-foreground">
                  <div>
                    <p className="font-semibold text-foreground mb-1">Entropía de Shannon</p>
                    <p>
                      {currentSession.metrics.shannon_entropy.toFixed(3)} bits/símbolo. Representa el límite teórico
                      mínimo de compresión posible.
                    </p>
                  </div>
                  <div>
                    <p className="font-semibold text-foreground mb-1">Longitud Media de Código</p>
                    <p>
                      {currentSession.metrics.average_code_length.toFixed(3)} bits/símbolo. Nuestro algoritmo logra
                      una compresión muy cercana al óptimo teórico.
                    </p>
                  </div>
                  <div>
                    <p className="font-semibold text-foreground mb-1">Eficiencia</p>
                    <p>
                      {currentSession.metrics.efficiency.toFixed(2)}%. Qué tan cerca estamos del límite teórico de
                      compresión óptima.
                    </p>
                  </div>
                  <div>
                    <p className="font-semibold text-foreground mb-1">Reducción</p>
                    <p>
                      Se redujo {currentSession.metrics.compression_ratio.toFixed(2)}% del tamaño original. El archivo
                      comprimido es significativamente más pequeño.
                    </p>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border mt-16 py-8 text-center text-sm text-muted-foreground">
        <p>
          Huffman Compressor Pro • Algoritmo de Compresión Huffman • Proyecto Académico • Universidad Pedagógica de
          Colombia
        </p>
      </footer>
    </div>
  )
}
