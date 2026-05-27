'use client'

import { motion } from 'framer-motion'
import type { FrequencyItem, CodeItem } from '@/types'
import { ChevronDown } from 'lucide-react'
import { useState } from 'react'

interface FrequencyTableProps {
  frequencies: FrequencyItem[]
}

interface CodeTableProps {
  codes: CodeItem[]
}

export function FrequencyTable({ frequencies }: FrequencyTableProps) {
  const [isExpanded, setIsExpanded] = useState(true)

  const sortedFrequencies = [...frequencies].sort((a, b) => b.frequency - a.frequency)

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="border border-border rounded-xl overflow-hidden bg-card/50 backdrop-blur"
    >
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-4 py-3 flex items-center justify-between bg-card border-b border-border hover:bg-card/70 transition-colors"
      >
        <h3 className="text-sm font-semibold text-foreground">Tabla de Frecuencias</h3>
        <ChevronDown
          className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
        />
      </button>

      {isExpanded && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-card/50 border-b border-border">
                <th className="px-4 py-3 text-left font-semibold text-muted-foreground">Carácter</th>
                <th className="px-4 py-3 text-right font-semibold text-muted-foreground">Frecuencia</th>
                <th className="px-4 py-3 text-right font-semibold text-muted-foreground">Porcentaje</th>
              </tr>
            </thead>
            <tbody>
              {sortedFrequencies.map((item, index) => (
                <motion.tr
                  key={index}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.02 }}
                  className="border-b border-border/50 hover:bg-primary/5 transition-colors"
                >
                  <td className="px-4 py-3 font-mono text-foreground">
                    {item.displayChar === ' ' ? '␣' : item.displayChar}
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-primary">{item.frequency}</td>
                  <td className="px-4 py-3 text-right text-muted-foreground">
                    {item.percentage.toFixed(2)}%
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </motion.div>
  )
}

export function CodeTable({ codes }: CodeTableProps) {
  const [isExpanded, setIsExpanded] = useState(true)

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
      className="border border-border rounded-xl overflow-hidden bg-card/50 backdrop-blur"
    >
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-4 py-3 flex items-center justify-between bg-card border-b border-border hover:bg-card/70 transition-colors"
      >
        <h3 className="text-sm font-semibold text-foreground">Tabla de Códigos Huffman</h3>
        <ChevronDown
          className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
        />
      </button>

      {isExpanded && (
        <div className="overflow-x-auto max-h-96">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-card/50 border-b border-border sticky top-0">
                <th className="px-4 py-3 text-left font-semibold text-muted-foreground">Carácter</th>
                <th className="px-4 py-3 text-left font-semibold text-muted-foreground">Código</th>
                <th className="px-4 py-3 text-right font-semibold text-muted-foreground">Bits</th>
                <th className="px-4 py-3 text-right font-semibold text-muted-foreground">Freq.</th>
                <th className="px-4 py-3 text-right font-semibold text-muted-foreground">Total Bits</th>
              </tr>
            </thead>
            <tbody>
              {codes.map((item, index) => (
                <motion.tr
                  key={index}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.01 }}
                  className="border-b border-border/50 hover:bg-primary/5 transition-colors"
                >
                  <td className="px-4 py-3 font-mono text-foreground">
                    {item.displayChar === ' ' ? '␣' : item.displayChar}
                  </td>
                  <td className="px-4 py-3 font-mono text-green-400 font-semibold text-sm">
                    {item.code}
                  </td>
                  <td className="px-4 py-3 text-right text-primary">{item.bits}</td>
                  <td className="px-4 py-3 text-right text-muted-foreground">{item.frequency}</td>
                  <td className="px-4 py-3 text-right font-semibold text-accent">
                    {item.size_in_bits}
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </motion.div>
  )
}
