export default function AlternativaCampos({ alternativa, onCambiarTexto, onCambiarImagen, onMarcarCorrecta, subiendo }) {
  return (
    <div className="alternativa-campos">
      <div className="alternativa-campos-cabecera">
        <label>
          <input
            type="radio"
            name="alternativa-correcta"
            checked={alternativa.es_correcta}
            onChange={() => onMarcarCorrecta(alternativa.etiqueta)}
          />{' '}
          {alternativa.etiqueta}) es la correcta
        </label>
      </div>
      <textarea
        value={alternativa.texto}
        onChange={(e) => onCambiarTexto(alternativa.etiqueta, e.target.value)}
        placeholder={`Texto de la alternativa ${alternativa.etiqueta} (soporta LaTeX)`}
        required
      />
      <input
        type="file"
        accept="image/png,image/jpeg,image/webp"
        onChange={(e) => e.target.files[0] && onCambiarImagen(alternativa.etiqueta, e.target.files[0])}
      />
      {subiendo && <p>Subiendo imagen…</p>}
      {alternativa.imagen_url && (
        <img src={alternativa.imagen_url} alt="" style={{ maxWidth: '100%', marginTop: 8 }} />
      )}
    </div>
  )
}
