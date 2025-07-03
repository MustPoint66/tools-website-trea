import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { ThemeProvider } from '@/components/theme-provider'
import { Toaster } from 'sonner'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Tools Mania - All Online Tools in One Place',
  description: 'Your ultimate destination for powerful online tools. Convert, calculate, format, and transform with ease. Document tools, image tools, text tools, calculators, and more.',
  icons: {
    icon: '/favicon.ico',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}): React.ReactElement {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
          {children}
          <Toaster 
            position="top-right"
            richColors
            expand
            closeButton
            duration={4000}
          />
        </ThemeProvider>
      </body>
    </html>
  )
}
