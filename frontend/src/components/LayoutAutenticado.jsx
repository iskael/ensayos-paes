import { useState, useCallback } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../AuthContext.jsx'
import { MENU_POR_ROL, ETIQUETA_ROL } from '../constantes.js'
import { aplicarTema, temaGuardado } from '../tema.js'
import Icono from './Icono.jsx'
import Hoja from './Hoja.jsx'

const TEMAS = [
  { valor: 'auto', etiqueta: 'Automático' },
  { valor: 'claro', etiqueta: 'Claro' },
  { valor: 'oscuro', etiqueta: 'Oscuro' },
]

export default function LayoutAutenticado({ children, sinNavegacion = false }) {
  const [cuentaAbierta, setCuentaAbierta] = useState(false)
  const [tema, setTema] = useState(temaGuardado)
  const { usuario, cerrarSesion } = useAuth()
  const navigate = useNavigate()
  const cerrarCuenta = useCallback(() => setCuentaAbierta(false), [])

  if (sinNavegacion) return <div className="layout-autenticado-sin-nav">{children}</div>

  function alCerrarSesion() {
    setCuentaAbierta(false)
    cerrarSesion()
    navigate('/login')
  }

  function elegirTema(valor) {
    setTema(valor)
    aplicarTema(valor)
  }

  const items = (MENU_POR_ROL[usuario?.rol] ?? []).filter((i) => i.disponible)
  const inicial = (usuario?.nombre ?? '?').trim().charAt(0).toUpperCase()

  return (
    <div className="layout-autenticado">
      <header className="barra-superior">
        <span className="barra-superior-titulo">
          Ensayos <span>PAES</span>
        </span>
        <button type="button" className="boton-icono" aria-label="Mi cuenta" onClick={() => setCuentaAbierta(true)}>
          <span className="avatar" style={{ width: 34, height: 34, fontSize: 14 }}>
            {inicial}
          </span>
        </button>
      </header>

      <main>{children}</main>

      <nav className="tabs" aria-label="Navegación principal">
        {items.map((item) => (
          <NavLink key={item.ruta} to={item.ruta} end className={({ isActive }) => 'tab' + (isActive ? ' activo' : '')}>
            <Icono nombre={item.icono} />
            {item.etiqueta}
          </NavLink>
        ))}
        <button type="button" className="tab" onClick={() => setCuentaAbierta(true)}>
          <Icono nombre="cuenta" />
          Cuenta
        </button>
      </nav>

      {cuentaAbierta && (
        <Hoja titulo="Mi cuenta" onCerrar={cerrarCuenta}>
          <div className="cuenta-usuario">
            <span className="avatar">{inicial}</span>
            <div>
              <strong>{usuario?.nombre}</strong>
              <div className="texto-suave" style={{ fontSize: 14 }}>
                {usuario?.email}
              </div>
              <span className="badge-rol">{ETIQUETA_ROL[usuario?.rol] ?? usuario?.rol}</span>
            </div>
          </div>
          <span className="etiqueta-campo">Apariencia</span>
          <div className="segmentos" style={{ marginBottom: 20 }}>
            {TEMAS.map((t) => (
              <button
                key={t.valor}
                type="button"
                className={'segmento' + (tema === t.valor ? ' activo' : '')}
                onClick={() => elegirTema(t.valor)}
              >
                {t.etiqueta}
              </button>
            ))}
          </div>
          <button className="boton-secundario" type="button" onClick={alCerrarSesion}>
            Cerrar sesión
          </button>
        </Hoja>
      )}
    </div>
  )
}
