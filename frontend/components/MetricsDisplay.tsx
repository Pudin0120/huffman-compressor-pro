'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts'
import { Card } from '@radix-ui/react-primitive'
import { motion } from 'framer-motion'
import type { CompressionMetrics } from '@/types'
import { FileText, HardDrive, Zap, TrendingDown } from 'lucide-react'

interface MetricsDisplayProps {
  metrics: CompressionMetrics
}

export default function MetricsDisplay({ metrics }: MetricsDisplayProps) {
  const metricsCards = [
    {
      label: 'Tamaño Original',
      value: `${(metrics.original_size / 1024).toFixed(2)} KB`,
      icon: FileText,
      color: 'text-blue-500',
      bgColor: 'bg-blue-500/10',
    },
    {
      label: 'Tamaño Comprimido',
      value: `${(metrics.compressed_size / 1024).toFixed(2)} KB`,
      icon: HardDrive,
      color: 'text-green-500',
      bgColor: 'bg-green-500/10',
    },
    {
      label: 'Ratio de Compresión',
      value: `${metrics.compression_ratio.toFixed(2)}%`,
      icon: TrendingDown,
      color: 'text-purple-500',
      bgColor: 'bg-purple-500/10',
    },
    {
      label: 'Eficiencia',
      value: `${metrics.efficiency.toFixed(2)}%`,
      icon: Zap,
      color: 'text-amber-500',
      bgColor: 'bg-amber-500/10',
    },
  ]

  const chartData = [
    {
      name: 'Tamaño',
      Original: metrics.original_size,
      Comprimido: metrics.compressed_size,
    },
  ]

  const metricsData = [
    {
      name: 'Entropía',
      value: metrics.shannon_entropy.toFixed(3),
      max: 8,
    },
    {
      name: 'Long. Media',
      value: metrics.average_code_length.toFixed(3),
      max: 8,
    },
    {
      name: 'Caracteres Únicos',
      value: metrics.unique_characters,
      max: 256,
    },
  ]

  return (
    <div className="space-y-6">
      {/* Tarjetas principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metricsCards.map((card, index) => {
          const Icon = card.icon
          return (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`${card.bgColor} border border-border rounded-xl p-4`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-muted-foreground uppercase tracking-wider">{card.label}</p>
                  <p className={`text-2xl font-bold ${card.color} mt-2`}>{card.value}</p>
                </div>
                <Icon className={`${card.color} w-8 h-8 opacity-50`} />
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Gráfico comparativo */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="border border-border rounded-xl p-4 bg-card/50"
      >
        <h3 className="text-sm font-semibold mb-4 text-foreground">Comparación de Tamaños (Bytes)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" />
            <YAxis stroke="hsl(var(--muted-foreground))" />
            <Tooltip
              contentStyle={{
                background: 'hsl(var(--card))',
                border: '1px solid hsl(var(--border))',
                borderRadius: '8px',
              }}
              cursor={{ fill: 'hsl(var(--primary)/0.1)' }}
            />
            <Legend />
            <Bar dataKey="Original" fill="hsl(var(--destructive))" radius={[8, 8, 0, 0]} />
            <Bar dataKey="Comprimido" fill="hsl(var(--primary))" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Detalles técnicos */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-4"
      >
        {metricsData.map((item, index) => (
          <div key={index} className="border border-border rounded-xl p-4 bg-card/50">
            <p className="text-xs text-muted-foreground uppercase tracking-wider">{item.name}</p>
            <div className="mt-3">
              <p className="text-2xl font-bold text-primary">{item.value}</p>
              <div className="mt-2 h-2 bg-border rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${(parseFloat(item.value.toString()) / item.max) * 100}%` }}
                  transition={{ duration: 0.8, delay: index * 0.1 }}
                  className="h-full bg-gradient-to-r from-green-500 to-emerald-500"
                />
              </div>
            </div>
          </div>
        ))}
      </motion.div>
    </div>
  )
}
