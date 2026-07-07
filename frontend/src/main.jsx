import React from 'react'
import { createRoot } from 'react-dom/client'
import Formula from './components/Formula.jsx'
import './styles.css'

function App() {
  return (
    <div className="pantalla">
      <div className="tarjeta">
        <Formula texto="Resuelve: $x^2 + 2x + 1 = 0$ y luego $$\int_0^1 x\,dx$$" />
      </div>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
