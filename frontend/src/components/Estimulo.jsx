import { useState } from 'react'
import { urlImagen } from '../api.js'
import Formula from './Formula.jsx'
import Icono from './Icono.jsx'

export default function Estimulo({ estimulo, numerar = false, abiertoInicial = true }) {
  const [abierto, setAbierto] = useState(abiertoInicial)
  const parrafos = estimulo.texto.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean)

  return (
    <aside className="estimulo" aria-label={estimulo.titulo ?? 'Texto de la pregunta'}>
      <button type="button" className="estimulo-alternar" aria-expanded={abierto} onClick={() => setAbierto((a) => !a)}>
        <span style={{ display: 'inline-flex', gap: 8, alignItems: 'center' }}>
          <Icono nombre="texto" tam={18} />
          {estimulo.titulo ?? 'Texto'}
        </span>
        <span className="texto-suave" style={{ fontSize: 14 }}>
          {abierto ? 'Ocultar' : 'Leer'}
        </span>
      </button>
      <div className="estimulo-texto" style={{ display: abierto ? 'block' : 'none' }}>
        {estimulo.titulo && <h3>{estimulo.titulo}</h3>}
        {estimulo.imagen_url && <img className="figura-item" src={urlImagen(estimulo.imagen_url)} alt="" />}
        {parrafos.map((p, i) =>
          numerar ? (
            <p key={i} className="parrafo-numerado">
              <span>{i + 1}</span>
              <span style={{ color: 'inherit', fontSize: 'inherit', paddingTop: 0 }}>
                <Formula texto={p} />
              </span>
            </p>
          ) : (
            <p key={i}>
              <Formula texto={p} />
            </p>
          ),
        )}
        {estimulo.fuente && <p className="estimulo-fuente">{estimulo.fuente}</p>}
      </div>
    </aside>
  )
}
