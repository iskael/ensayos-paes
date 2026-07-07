import { InlineMath, BlockMath } from 'react-katex'
import 'katex/dist/katex.min.css'
import { partirTexto } from '../formula.js'

export default function Formula({ texto }) {
  const partes = partirTexto(texto)
  return (
    <>
      {partes.map((parte, indice) => {
        if (parte.tipo === 'bloque') return <BlockMath key={indice} math={parte.valor} />
        if (parte.tipo === 'inline') return <InlineMath key={indice} math={parte.valor} />
        return <span key={indice}>{parte.valor}</span>
      })}
    </>
  )
}
