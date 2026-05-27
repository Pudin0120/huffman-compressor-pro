'use client'

import { useEffect, useRef } from 'react'
import * as d3 from 'd3'
import { motion } from 'framer-motion'

interface TreeNode {
  char?: string
  freq: number
  left?: TreeNode
  right?: TreeNode
  code?: string
  id?: string
}

interface HuffmanTreeVisualizerProps {
  treeData?: {
    frequencies: Array<{ char: string; frequency: number }>
    codes: Array<{ char: string; code: string }>
    unique_chars: number
  }
}

export default function HuffmanTreeVisualizer({ treeData }: HuffmanTreeVisualizerProps) {
  const svgRef = useRef<SVGSVGElement>(null)

  useEffect(() => {
    if (!treeData || !svgRef.current) return

    // Para esta versión, mostrar una visualización simplificada
    const width = 800
    const height = 500
    const margin = { top: 20, right: 20, bottom: 20, left: 20 }

    d3.select(svgRef.current).selectAll('*').remove()

    const svg = d3
      .select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .style('background', 'hsl(var(--card))')

    // Crear visualización de los códigos
    const codes = treeData.codes.slice(0, 16) // Limitar a 16 para visualización
    const charHeight = 25
    const totalHeight = codes.length * charHeight + 40

    svg.attr('height', Math.max(height, totalHeight))

    // Título
    svg
      .append('text')
      .attr('x', width / 2)
      .attr('y', 25)
      .attr('text-anchor', 'middle')
      .attr('class', 'text-lg font-semibold')
      .attr('fill', 'hsl(var(--foreground))')
      .text('Árbol de Huffman - Vista de Códigos')

    // Grupo para los elementos
    const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top + 30})`)

    // Mostrar códigos
    codes.forEach((code, index) => {
      const y = index * charHeight

      // Carácter
      g.append('text')
        .attr('x', 20)
        .attr('y', y + 18)
        .attr('fill', 'hsl(var(--primary))')
        .attr('class', 'font-semibold')
        .text(`'${code.char === ' ' ? '␣' : code.char}'`)

      // Código
      g.append('text')
        .attr('x', 80)
        .attr('y', y + 18)
        .attr('fill', 'hsl(var(--accent))')
        .attr('class', 'font-mono')
        .text(code.code)

      // Barra de visualización
      const barWidth = code.code.length * 15
      g.append('rect')
        .attr('x', 200)
        .attr('y', y + 5)
        .attr('width', 0)
        .attr('height', 15)
        .attr('fill', 'hsl(var(--primary))')
        .attr('rx', 3)
        .transition()
        .duration(500)
        .delay(index * 30)
        .attr('width', barWidth)

      // Longitud de código
      g.append('text')
        .attr('x', 200 + barWidth + 10)
        .attr('y', y + 18)
        .attr('fill', 'hsl(var(--muted-foreground))')
        .attr('class', 'text-sm')
        .text(`${code.code.length} bits`)
    })
  }, [treeData])

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="border border-border rounded-xl overflow-hidden bg-card/50 backdrop-blur p-4"
    >
      <h3 className="text-sm font-semibold text-foreground mb-4">Visualización del Árbol</h3>
      <div className="overflow-x-auto">
        <svg ref={svgRef} className="w-full" />
      </div>
      <p className="text-xs text-muted-foreground mt-4">
        La visualización muestra los códigos Huffman generados para cada carácter. Los códigos más cortos
        corresponden a caracteres más frecuentes, optimizando la compresión.
      </p>
    </motion.div>
  )
}
