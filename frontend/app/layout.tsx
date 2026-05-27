import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Providers from './providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Huffman Compressor Pro - Compresión de Archivos',
  description: 'Aplicación web profesional para comprimir y descomprimir archivos usando el algoritmo de Huffman',
  keywords: ['Huffman', 'Compresión', 'Algoritmo', 'Educación'],
  authors: [{ name: 'Joseff Antonio Laverde', url: 'https://github.com' }],
  viewport: 'width=device-width, initial-scale=1.0',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              if (localStorage.getItem('theme') === 'light' || 
                  (!('theme' in localStorage) && !window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                document.documentElement.classList.remove('dark')
              } else {
                document.documentElement.classList.add('dark')
              }
            `,
          }}
        />
      </head>
      <body className={`${inter.className} bg-background text-foreground`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
