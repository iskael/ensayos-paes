import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../AuthContext.jsx'
import { MENU_POR_ROL, ETIQUETA_ROL } from '../constantes.js'

export default function LayoutAutenticado({ children }) {
  const [abierto, setAbierto] = useState(false)
  const { usuario, cerrarSesion } = useAuth()
  const navigate = useNavigate()
  const drawerRef = useRef(null)
  const hamburguesaRef = useRef(null)

  useEffect(() => {
    if (!abierto) return
    const drawer = drawerRef.current
    drawer?.querySelector('.drawer-cerrar')?.focus()

    function alPresionarTecla(evento) {
      if (evento.key === 'Escape') {
        setAbierto(false)
        return
      }
      if (evento.key !== 'Tab' || !drawer) return
      const enfocables = drawer.querySelectorAll('a[href], button:not([disabled])')
      if (enfocables.length === 0) return
      const primero = enfocables[0]
      const ultimo = enfocables[enfocables.length - 1]
      if (evento.shiftKey && document.activeElement === primero) {
        evento.preventDefault()
        ultimo.focus()
      } else if (!evento.shiftKey && document.activeElement === ultimo) {
        evento.preventDefault()
        primero.focus()
      }
    }

    document.addEventListener('keydown', alPresionarTecla)
    return () => {
      document.removeEventListener('keydown', alPresionarTecla)
      hamburguesaRef.current?.focus()
    }
  }, [abierto])

  function alCerrarSesion() {
    setAbierto(false)
    cerrarSesion()
    navigate('/login')
  }

  const items = MENU_POR_ROL[usuario?.rol] ?? []

  return (
    <div className="layout-autenticado">
      <header className="barra-superior">
        <span className="barra-superior-titulo">Ensayos PAES</span>
        <button
          ref={hamburguesaRef}
          className="boton-hamburguesa"
          type="button"
          aria-label="Abrir menú"
          aria-expanded={abierto}
          onClick={() => setAbierto(true)}
        >
          ☰
        </button>
      </header>

      {abierto && (
        <div className="drawer-overlay" onClick={() => setAbierto(false)}>
          <nav
            ref={drawerRef}
            className="drawer"
            role="dialog"
            aria-modal="true"
            aria-label="Menú de usuario"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="drawer-cerrar"
              type="button"
              aria-label="Cerrar menú"
              onClick={() => setAbierto(false)}
            >
              ✕
            </button>

            <div className="drawer-usuario">
              <p className="drawer-usuario-nombre">{usuario?.nombre}</p>
              <p className="drawer-usuario-email">{usuario?.email}</p>
              <span className="badge-rol">{ETIQUETA_ROL[usuario?.rol] ?? usuario?.rol}</span>
            </div>

            <ul className="drawer-links">
              {items.map((item) => (
                <li key={item.etiqueta}>
                  {item.disponible ? (
                    <Link to={item.ruta} onClick={() => setAbierto(false)}>
                      {item.etiqueta}
                    </Link>
                  ) : (
                    <span className="drawer-link-deshabilitado">{item.etiqueta}</span>
                  )}
                </li>
              ))}
            </ul>

            <button className="boton drawer-logout" type="button" onClick={alCerrarSesion}>
              Cerrar sesión
            </button>
          </nav>
        </div>
      )}

      <main>{children}</main>
    </div>
  )
}
