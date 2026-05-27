'use client'

import { useState } from 'react'
import { FileUp, Download, Zap } from 'lucide-react'
import { motion } from 'framer-motion'
import { compressionApi } from '@/lib/api'
import { useCompressionStore } from '@/lib/store'
import toast from 'react-hot-toast'

export default function FileUploadZone() {
  const [isDragging, setIsDragging] = useState(false)
  const { setCurrentSession, setIsCompressing, setError } = useCompressionStore()

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const processFile = async (file: File) => {
    try {
      setIsCompressing(true)
      setError(null)

      if (!file.name.toLowerCase().endsWith('.txt') && !file.name.toLowerCase().endsWith('.huff')) {
        throw new Error('Solo se aceptan archivos .txt o .huff')
      }

      let response
      if (file.name.toLowerCase().endsWith('.huff')) {
        response = await compressionApi.decompressFile(file)
        toast.success('Archivo descomprimido exitosamente')
      } else {
        response = await compressionApi.compressFile(file)
        toast.success('Archivo comprimido exitosamente')
      }

      // Obtener sesión completa
      const session = await compressionApi.getSession(response.session_id)
      setCurrentSession(session)
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Error desconocido'
      setError(message)
      toast.error(message)
    } finally {
      setIsCompressing(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const files = e.dataTransfer.files
    if (files.length > 0) {
      processFile(files[0])
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.currentTarget.files
    if (files && files.length > 0) {
      processFile(files[0])
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`relative p-8 rounded-2xl border-2 border-dashed transition-all cursor-pointer ${
        isDragging
          ? 'border-primary bg-primary/5 shadow-glow'
          : 'border-border bg-card/50 hover:bg-card/70'
      }`}
    >
      <input
        type="file"
        accept=".txt,.huff"
        onChange={handleFileSelect}
        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
      />

      <div className="flex flex-col items-center justify-center space-y-4 text-center">
        <motion.div
          animate={{ scale: isDragging ? 1.1 : 1 }}
          transition={{ type: 'spring', stiffness: 300 }}
        >
          <FileUp className="w-12 h-12 text-primary mx-auto" />
        </motion.div>
        
        <div>
          <p className="text-lg font-semibold text-foreground">
            Arrastra tu archivo aquí
          </p>
          <p className="text-sm text-muted-foreground mt-1">
            O haz clic para seleccionar (.txt o .huff)
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs text-muted-foreground pt-2">
          <Zap className="w-3 h-3" />
          <span>Comprime automáticamente al subir</span>
        </div>
      </div>
    </motion.div>
  )
}
