'use client'

import { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'

// ─── Tipos ────────────────────────────────────────────────────────────────────

interface CodeItem {
  char: string
  displayChar: string
  code: string
  bits: number
  frequency: number
}

interface TreeVisualizerProps {
  treeData?: {
    frequencies: Array<{ char: string; frequency: number; displayChar?: string }>
    codes: CodeItem[]
    unique_chars: number
  }
}

interface TreeNode {
  id: string
  char?: string        // solo en hojas
  displayChar?: string
  frequency: number
  code: string         // código acumulado desde la raíz
  left?: TreeNode
  right?: TreeNode
  x: number
  y: number
  depth: number
}

// ─── Construcción del árbol desde los códigos Huffman ─────────────────────────

function buildTreeFromCodes(codes: CodeItem[]): TreeNode | null {
  if (!codes || codes.length === 0) return null

  // Raíz virtual
  const root: TreeNode = {
    id: 'root',
    frequency: 0,
    code: '',
    x: 0, y: 0, depth: 0,
  }

  // Insertar cada hoja según su código binario
  for (const item of codes) {
    let current = root
    const bits = item.code

    for (let i = 0; i < bits.length; i++) {
      const bit = bits[i]
      const isLast = i === bits.length - 1
      const childId = current.id + bit

      if (bit === '0') {
        if (!current.left) {
          current.left = {
            id: childId,
            frequency: 0,
            code: bits.slice(0, i + 1),
            x: 0, y: 0, depth: i + 1,
          }
        }
        if (isLast) {
          current.left.char = item.char
          current.left.displayChar = item.displayChar
          current.left.frequency = item.frequency
        }
        current = current.left
      } else {
        if (!current.right) {
          current.right = {
            id: childId,
            frequency: 0,
            code: bits.slice(0, i + 1),
            x: 0, y: 0, depth: i + 1,
          }
        }
        if (isLast) {
          current.right.char = item.char
          current.right.displayChar = item.displayChar
          current.right.frequency = item.frequency
        }
        current = current.right
      }
    }
  }

  // Calcular frecuencias de nodos internos (suma de hijos)
  function calcFreq(node: TreeNode): number {
    if (node.char !== undefined) return node.frequency
    const l = node.left ? calcFreq(node.left) : 0
    const r = node.right ? calcFreq(node.right) : 0
    node.frequency = l + r
    return node.frequency
  }
  calcFreq(root)

  return root
}

// ─── Layout Reingold-Tilford simplificado ─────────────────────────────────────

const NODE_RADIUS = 22
const LEVEL_HEIGHT = 80
const MIN_SIBLING_GAP = 56

function assignPositions(node: TreeNode | undefined, depth: number, minX: number): number {
  if (!node) return minX

  node.depth = depth
  node.y = depth * LEVEL_HEIGHT + NODE_RADIUS + 20

  const isLeaf = !node.left && !node.right

  if (isLeaf) {
    node.x = minX + NODE_RADIUS
    return minX + NODE_RADIUS * 2 + MIN_SIBLING_GAP
  }

  let curX = minX
  if (node.left) curX = assignPositions(node.left, depth + 1, curX)
  if (node.right) curX = assignPositions(node.right, depth + 1, curX + MIN_SIBLING_GAP * 0.3)

  // Centro del nodo entre sus hijos
  const leftX = node.left ? node.left.x : curX
  const rightX = node.right ? node.right.x : curX
  node.x = (leftX + rightX) / 2

  return curX
}

function flattenTree(node: TreeNode | undefined, acc: TreeNode[] = []): TreeNode[] {
  if (!node) return acc
  acc.push(node)
  flattenTree(node.left, acc)
  flattenTree(node.right, acc)
  return acc
}

interface Edge {
  x1: number; y1: number; x2: number; y2: number; label: string
}
function collectEdges(node: TreeNode | undefined, acc: Edge[] = []): Edge[] {
  if (!node) return acc
  if (node.left) {
    acc.push({ x1: node.x, y1: node.y, x2: node.left.x, y2: node.left.y, label: '0' })
    collectEdges(node.left, acc)
  }
  if (node.right) {
    acc.push({ x1: node.x, y1: node.y, x2: node.right.x, y2: node.right.y, label: '1' })
    collectEdges(node.right, acc)
  }
  return acc
}

// ─── Componente Principal ─────────────────────────────────────────────────────

export default function HuffmanTreeVisualizer({ treeData }: TreeVisualizerProps) {
  const svgRef = useRef<SVGSVGElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const [viewBox, setViewBox] = useState('0 0 900 500')
  const [tooltip, setTooltip] = useState<{ x: number; y: number; node: TreeNode } | null>(null)

  // Límite de hojas para que el árbol sea legible
  const MAX_LEAVES = 20

  const codesForTree = treeData
    ? [...treeData.codes]
        .sort((a, b) => b.frequency - a.frequency)
        .slice(0, MAX_LEAVES)
    : []

  const root = buildTreeFromCodes(codesForTree)

  useEffect(() => {
    if (!root) return
    assignPositions(root, 0, 20)

    const nodes = flattenTree(root)
    const maxX = Math.max(...nodes.map(n => n.x)) + NODE_RADIUS + 20
    const maxY = Math.max(...nodes.map(n => n.y)) + NODE_RADIUS + 30

    setViewBox(`0 0 ${Math.max(maxX, 600)} ${Math.max(maxY, 300)}`)
  }, [treeData])

  if (!treeData || !root) {
    return (
      <div className="border border-border rounded-xl p-6 bg-card/50 text-center text-muted-foreground text-sm">
        Comprime un archivo para visualizar el árbol de Huffman.
      </div>
    )
  }

  // Re-asignar posiciones en cada render para que el viewBox esté actualizado
  assignPositions(root, 0, 20)
  const nodes = flattenTree(root)
  const edges = collectEdges(root)

  const totalShown = codesForTree.length
  const totalChars = treeData.codes.length

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="border border-border rounded-xl overflow-hidden bg-card/50 backdrop-blur p-4"
    >
      {/* Encabezado */}
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-foreground">🌳 Árbol de Huffman Interactivo</h3>
        {totalChars > MAX_LEAVES && (
          <span className="text-xs text-amber-400 bg-amber-400/10 px-2 py-1 rounded-full">
            Mostrando {totalShown} de {totalChars} caracteres (los más frecuentes)
          </span>
        )}
      </div>

      {/* Leyenda */}
      <div className="flex gap-4 mb-3 text-xs text-muted-foreground">
        <span className="flex items-center gap-1">
          <span className="inline-block w-3 h-3 rounded-full bg-emerald-500"></span> Hoja (carácter)
        </span>
        <span className="flex items-center gap-1">
          <span className="inline-block w-3 h-3 rounded-full bg-slate-500"></span> Nodo interno
        </span>
        <span className="flex items-center gap-1 text-blue-400">← 0 &nbsp; 1 →</span>
      </div>

      {/* SVG del árbol */}
      <div ref={containerRef} className="overflow-x-auto overflow-y-auto max-h-[520px] rounded-lg bg-slate-900/60">
        <svg
          ref={svgRef}
          viewBox={viewBox}
          className="min-w-full"
          style={{ minHeight: 280 }}
        >
          <defs>
            {/* Gradiente para hojas */}
            <radialGradient id="leafGrad" cx="40%" cy="35%">
              <stop offset="0%" stopColor="#34d399" />
              <stop offset="100%" stopColor="#059669" />
            </radialGradient>
            {/* Gradiente para nodos internos */}
            <radialGradient id="internalGrad" cx="40%" cy="35%">
              <stop offset="0%" stopColor="#475569" />
              <stop offset="100%" stopColor="#1e293b" />
            </radialGradient>
            {/* Sombra */}
            <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#000" floodOpacity="0.4" />
            </filter>
          </defs>

          {/* ── Aristas ── */}
          {edges.map((e, i) => {
            const mx = (e.x1 + e.x2) / 2
            const my = (e.y1 + e.y2) / 2
            return (
              <g key={`edge-${i}`}>
                <line
                  x1={e.x1} y1={e.y1}
                  x2={e.x2} y2={e.y2}
                  stroke={e.label === '0' ? '#3b82f6' : '#f59e0b'}
                  strokeWidth={1.8}
                  strokeOpacity={0.7}
                />
                {/* Etiqueta 0/1 en la mitad de la arista */}
                <circle cx={mx} cy={my} r={9} fill={e.label === '0' ? '#1d4ed8' : '#b45309'} />
                <text
                  x={mx} y={my + 4}
                  textAnchor="middle"
                  fontSize={10}
                  fontWeight="bold"
                  fill="white"
                >
                  {e.label}
                </text>
              </g>
            )
          })}

          {/* ── Nodos ── */}
          {nodes.map(node => {
            const isLeaf = !node.left && !node.right
            const label = node.char !== undefined
              ? (node.displayChar || (node.char === ' ' ? '␣' : node.char))
              : '·'

            return (
              <g
                key={node.id}
                style={{ cursor: 'pointer' }}
                onMouseEnter={() => setTooltip({ x: node.x, y: node.y, node })}
                onMouseLeave={() => setTooltip(null)}
              >
                {/* Círculo principal */}
                <circle
                  cx={node.x}
                  cy={node.y}
                  r={NODE_RADIUS}
                  fill={isLeaf ? 'url(#leafGrad)' : 'url(#internalGrad)'}
                  stroke={isLeaf ? '#10b981' : '#475569'}
                  strokeWidth={isLeaf ? 2 : 1}
                  filter="url(#shadow)"
                />

                {/* Texto del nodo */}
                {isLeaf ? (
                  <>
                    <text
                      x={node.x} y={node.y - 3}
                      textAnchor="middle"
                      fontSize={label.length > 1 ? 9 : 13}
                      fontWeight="bold"
                      fill="white"
                    >
                      {label}
                    </text>
                    <text
                      x={node.x} y={node.y + 12}
                      textAnchor="middle"
                      fontSize={8}
                      fill="#a7f3d0"
                    >
                      {node.frequency}
                    </text>
                  </>
                ) : (
                  <text
                    x={node.x} y={node.y + 4}
                    textAnchor="middle"
                    fontSize={9}
                    fill="#94a3b8"
                  >
                    {node.frequency}
                  </text>
                )}

                {/* Badge del código en hojas */}
                {isLeaf && node.code && (
                  <text
                    x={node.x}
                    y={node.y + NODE_RADIUS + 13}
                    textAnchor="middle"
                    fontSize={7}
                    fill="#fbbf24"
                    fontFamily="monospace"
                  >
                    {node.code.length > 8 ? node.code.slice(0, 7) + '…' : node.code}
                  </text>
                )}
              </g>
            )
          })}

          {/* ── Tooltip ── */}
          {tooltip && (() => {
            const n = tooltip.node
            const isLeaf = !n.left && !n.right
            const tx = n.x + NODE_RADIUS + 8
            const ty = n.y - 30
            const w = 120, h = isLeaf ? 62 : 42
            return (
              <g>
                <rect
                  x={tx - 4} y={ty - 14}
                  width={w} height={h}
                  rx={6}
                  fill="#0f172a"
                  stroke="#334155"
                  strokeWidth={1}
                  opacity={0.95}
                />
                {isLeaf && (
                  <text x={tx} y={ty} fontSize={11} fill="#10b981" fontWeight="bold">
                    Char: '{n.displayChar || (n.char === ' ' ? '␣' : n.char)}'
                  </text>
                )}
                <text x={tx} y={ty + (isLeaf ? 15 : 0)} fontSize={10} fill="#94a3b8">
                  Frecuencia: {n.frequency}
                </text>
                {isLeaf && (
                  <>
                    <text x={tx} y={ty + 30} fontSize={10} fill="#fbbf24" fontFamily="monospace">
                      Código: {n.code}
                    </text>
                    <text x={tx} y={ty + 44} fontSize={10} fill="#94a3b8">
                      {n.code.length} bits
                    </text>
                  </>
                )}
              </g>
            )
          })()}
        </svg>
      </div>

      <p className="text-xs text-muted-foreground mt-3">
        Pasa el cursor sobre un nodo para ver sus detalles. Los nodos verdes son hojas (caracteres);
        los grises son nodos internos. La rama azul representa el bit <strong>0</strong> y la ámbar el bit <strong>1</strong>.
      </p>
    </motion.div>
  )
}
