import { useEffect, useRef } from 'react'
import Icono from './Icono.jsx'

export default function Hoja({ titulo, onCerrar, children }) {
  const ref = useRef(null)

  useEffect(() => {
    const previo = document.activeElement
    ref.current?.focus()
    function alTeclear(e) {
      if (e.key === 'Escape') onCerrar()
    }
    document.addEventListener('keydown', alTeclear)
    const overflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      document.removeEventListener('keydown', alTeclear)
      document.body.style.overflow = overflow
      previo?.focus?.()
    }
  }, [onCerrar])

  return (
    <div className="hoja-fondo" onClick={onCerrar}>
      <div
        className="hoja"
        role="dialog"
        aria-modal="true"
        aria-label={titulo}
        tabIndex={-1}
        ref={ref}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="hoja-cabecera">
          <h2>{titulo}</h2>
          <button type="button" className="boton-icono" aria-label="Cerrar" onClick={onCerrar}>
            <Icono nombre="cerrar" />
          </button>
        </div>
        {children}
      </div>
    </div>
  )
}
