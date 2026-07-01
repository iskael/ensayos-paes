package httpx

import (
	"errors"
	"net/http"
	"strconv"
	"time"

	"github.com/go-chi/chi/v5"

	"github.com/usuario/ensayos-paes/internal/domain"
	"github.com/usuario/ensayos-paes/internal/pdfimport"
	"github.com/usuario/ensayos-paes/internal/repo"
	"github.com/usuario/ensayos-paes/internal/storage"
)

type bancoHandler struct {
	examenes *repo.Examenes
	items    *repo.Items
	clave    *repo.Clave
	imagenes *storage.Imagenes
}

func paginacion(r *http.Request) (int, int) {
	limit, offset := 20, 0
	if v := r.URL.Query().Get("limit"); v != "" {
		if n, err := strconv.Atoi(v); err == nil && n > 0 && n <= 100 {
			limit = n
		}
	}
	if v := r.URL.Query().Get("offset"); v != "" {
		if n, err := strconv.Atoi(v); err == nil && n >= 0 {
			offset = n
		}
	}
	return limit, offset
}

// ---------------- Exámenes ----------------

type examenInput struct {
	Nombre           string  `json:"nombre"`
	AnioAdmision     int     `json:"anio_admision"`
	Tipo             string  `json:"tipo"`
	Nivel            string  `json:"nivel"`
	Edicion          *string `json:"edicion"`
	URLPdf           *string `json:"url_pdf"`
	FechaPublicacion *string `json:"fecha_publicacion"`
}

func (in examenInput) aDominio() (domain.ExamenFuente, error) {
	tipo := domain.TipoExamen(in.Tipo)
	nivel := domain.Nivel(in.Nivel)
	if in.Nombre == "" || in.AnioAdmision == 0 || !tipo.Valido() || !nivel.Valido() {
		return domain.ExamenFuente{}, errors.New("nombre, anio_admision, tipo o nivel inválidos")
	}
	e := domain.ExamenFuente{
		Nombre:       in.Nombre,
		AnioAdmision: in.AnioAdmision,
		Tipo:         tipo,
		Nivel:        nivel,
		Edicion:      in.Edicion,
		URLPdf:       in.URLPdf,
	}
	if in.FechaPublicacion != nil && *in.FechaPublicacion != "" {
		t, err := time.Parse("2006-01-02", *in.FechaPublicacion)
		if err != nil {
			return domain.ExamenFuente{}, errors.New("fecha_publicacion inválida (usar YYYY-MM-DD)")
		}
		e.FechaPublicacion = &t
	}
	return e, nil
}

func (h *bancoHandler) crearExamen(w http.ResponseWriter, r *http.Request) {
	var in examenInput
	if !decodificar(w, r, &in) {
		return
	}
	e, err := in.aDominio()
	if err != nil {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", err.Error())
		return
	}
	creado, err := h.examenes.Crear(r.Context(), e)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo crear el examen")
		return
	}
	escribirJSON(w, http.StatusCreated, creado)
}

func (h *bancoHandler) listarExamenes(w http.ResponseWriter, r *http.Request) {
	limit, offset := paginacion(r)
	lista, err := h.examenes.Listar(r.Context(), limit, offset)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo listar exámenes")
		return
	}
	escribirJSON(w, http.StatusOK, lista)
}

func (h *bancoHandler) obtenerExamen(w http.ResponseWriter, r *http.Request) {
	e, err := h.examenes.PorID(r.Context(), chi.URLParam(r, "examenId"))
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Examen no encontrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "Error al obtener el examen")
		return
	}
	escribirJSON(w, http.StatusOK, e)
}

func (h *bancoHandler) actualizarExamen(w http.ResponseWriter, r *http.Request) {
	var in examenInput
	if !decodificar(w, r, &in) {
		return
	}
	e, err := in.aDominio()
	if err != nil {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", err.Error())
		return
	}
	actualizado, err := h.examenes.Actualizar(r.Context(), chi.URLParam(r, "examenId"), e)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Examen no encontrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo actualizar el examen")
		return
	}
	escribirJSON(w, http.StatusOK, actualizado)
}

func (h *bancoHandler) eliminarExamen(w http.ResponseWriter, r *http.Request) {
	err := h.examenes.Eliminar(r.Context(), chi.URLParam(r, "examenId"))
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Examen no encontrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo eliminar el examen")
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ---------------- Clave de corrección ----------------

type claveItemInput struct {
	ItemID string `json:"item_id"`
	Peso   int    `json:"peso"`
}

type claveInput struct {
	Pesos []claveItemInput `json:"pesos"`
}

func claveResp(examenID string, ce repo.ClaveEstado) map[string]any {
	pesos := make([]claveItemInput, 0, len(ce.Pesos))
	for _, p := range ce.Pesos {
		pesos = append(pesos, claveItemInput{ItemID: p.ItemID, Peso: p.Peso})
	}
	return map[string]any{
		"examen_id":  examenID,
		"suma_pesos": ce.SumaPesosPublicados,
		"valida":     ce.Valida,
		"pesos":      pesos,
	}
}

func (h *bancoHandler) obtenerClave(w http.ResponseWriter, r *http.Request) {
	examenID := chi.URLParam(r, "examenId")
	if _, err := h.examenes.PorID(r.Context(), examenID); errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Examen no encontrado")
		return
	}
	ce, err := h.clave.Obtener(r.Context(), examenID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo obtener la clave")
		return
	}
	escribirJSON(w, http.StatusOK, claveResp(examenID, ce))
}

// definirClave valida que la suma de los pesos enviados sea 1000 (RN-03).
func (h *bancoHandler) definirClave(w http.ResponseWriter, r *http.Request) {
	examenID := chi.URLParam(r, "examenId")
	var in claveInput
	if !decodificar(w, r, &in) {
		return
	}

	pesosVal := make([]int, 0, len(in.Pesos))
	pesos := make([]repo.PesoItem, 0, len(in.Pesos))
	for _, p := range in.Pesos {
		if p.Peso < 0 {
			escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "El peso no puede ser negativo")
			return
		}
		pesosVal = append(pesosVal, p.Peso)
		pesos = append(pesos, repo.PesoItem{ItemID: p.ItemID, Peso: p.Peso})
	}
	if domain.SumaPesos(pesosVal) != domain.PesoTotalClave {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "La suma de los pesos debe ser 1000")
		return
	}

	if err := h.clave.ActualizarPesos(r.Context(), examenID, pesos); err != nil {
		if errors.Is(err, repo.ErrNoEncontrado) {
			escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Algún ítem no pertenece a este examen")
			return
		}
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo guardar la clave")
		return
	}

	ce, err := h.clave.Obtener(r.Context(), examenID)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo releer la clave")
		return
	}
	escribirJSON(w, http.StatusOK, claveResp(examenID, ce))
}

// ---------------- Ítems ----------------

type alternativaInput struct {
	Etiqueta   string  `json:"etiqueta"`
	Texto      string  `json:"texto"`
	ImagenURL  *string `json:"imagen_url"`
	EsCorrecta bool    `json:"es_correcta"`
}

type itemInput struct {
	ExamenFuenteID *string             `json:"examen_fuente_id"`
	Enunciado      string              `json:"enunciado"`
	ImagenURL      *string             `json:"imagen_url"`
	Eje            string              `json:"eje"`
	Nivel          string              `json:"nivel"`
	Dificultad     string              `json:"dificultad"`
	Peso           *int                `json:"peso"`
	Explicacion    *string             `json:"explicacion"`
	Alternativas   []alternativaInput  `json:"alternativas"`
}

func (in itemInput) aDominio() (domain.Item, error) {
	eje := domain.Eje(in.Eje)
	nivel := domain.Nivel(in.Nivel)
	dificultad := domain.Dificultad(in.Dificultad)
	if in.Enunciado == "" || !eje.Valido() || !nivel.Valido() || !dificultad.Valido() {
		return domain.Item{}, errors.New("enunciado, eje, nivel o dificultad inválidos")
	}
	alts := make([]domain.Alternativa, 0, len(in.Alternativas))
	for _, a := range in.Alternativas {
		alts = append(alts, domain.Alternativa{
			Etiqueta:   domain.EtiquetaAlternativa(a.Etiqueta),
			Texto:      a.Texto,
			ImagenURL:  a.ImagenURL,
			EsCorrecta: a.EsCorrecta,
		})
	}
	if err := domain.ValidarAlternativas(alts); err != nil {
		return domain.Item{}, err
	}
	return domain.Item{
		ExamenFuenteID: in.ExamenFuenteID,
		Enunciado:      in.Enunciado,
		ImagenURL:      in.ImagenURL,
		Eje:            eje,
		Nivel:          nivel,
		Dificultad:     dificultad,
		Peso:           in.Peso,
		Explicacion:    in.Explicacion,
		Alternativas:   alts,
	}, nil
}

func (h *bancoHandler) crearItem(w http.ResponseWriter, r *http.Request) {
	var in itemInput
	if !decodificar(w, r, &in) {
		return
	}
	it, err := in.aDominio()
	if err != nil {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", err.Error())
		return
	}
	it.Origen = domain.OrigenOficial
	creado, err := h.items.Crear(r.Context(), it)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo crear el ítem")
		return
	}
	escribirJSON(w, http.StatusCreated, creado)
}

func (h *bancoHandler) listarItems(w http.ResponseWriter, r *http.Request) {
	limit, offset := paginacion(r)
	f := repo.FiltrosItems{Limit: limit, Offset: offset}
	q := r.URL.Query()
	if v := q.Get("nivel"); v != "" {
		n := domain.Nivel(v)
		f.Nivel = &n
	}
	if v := q.Get("eje"); v != "" {
		e := domain.Eje(v)
		f.Eje = &e
	}
	if v := q.Get("dificultad"); v != "" {
		d := domain.Dificultad(v)
		f.Dificultad = &d
	}
	if v := q.Get("estado"); v != "" {
		e := domain.EstadoItem(v)
		f.Estado = &e
	}
	if v := q.Get("examenId"); v != "" {
		f.ExamenID = &v
	}
	lista, err := h.items.Listar(r.Context(), f)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo listar ítems")
		return
	}
	escribirJSON(w, http.StatusOK, lista)
}

func (h *bancoHandler) obtenerItem(w http.ResponseWriter, r *http.Request) {
	it, err := h.items.PorID(r.Context(), chi.URLParam(r, "itemId"))
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Ítem no encontrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "Error al obtener el ítem")
		return
	}
	escribirJSON(w, http.StatusOK, it)
}

func (h *bancoHandler) actualizarItem(w http.ResponseWriter, r *http.Request) {
	var in itemInput
	if !decodificar(w, r, &in) {
		return
	}
	it, err := in.aDominio()
	if err != nil {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", err.Error())
		return
	}
	actualizado, err := h.items.Actualizar(r.Context(), chi.URLParam(r, "itemId"), it)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Ítem no encontrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo actualizar el ítem")
		return
	}
	escribirJSON(w, http.StatusOK, actualizado)
}

func (h *bancoHandler) eliminarItem(w http.ResponseWriter, r *http.Request) {
	err := h.items.Eliminar(r.Context(), chi.URLParam(r, "itemId"))
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Ítem no encontrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo eliminar el ítem")
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// publicarItem exige peso asignado y 4 alternativas válidas (RN-04).
func (h *bancoHandler) publicarItem(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "itemId")
	it, err := h.items.PorID(r.Context(), id)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Ítem no encontrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "Error al obtener el ítem")
		return
	}
	if it.Peso == nil || *it.Peso <= 0 {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "El ítem no tiene un peso asignado")
		return
	}
	if err := domain.ValidarAlternativas(it.Alternativas); err != nil {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", err.Error())
		return
	}
	publicado, err := h.items.CambiarEstado(r.Context(), id, domain.EstadoPublicado)
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo publicar el ítem")
		return
	}
	escribirJSON(w, http.StatusOK, publicado)
}

func (h *bancoHandler) ocultarItem(w http.ResponseWriter, r *http.Request) {
	oculto, err := h.items.CambiarEstado(r.Context(), chi.URLParam(r, "itemId"), domain.EstadoOculto)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Ítem no encontrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "No se pudo ocultar el ítem")
		return
	}
	escribirJSON(w, http.StatusOK, oculto)
}

// ---------------- Importación de PDF (asistida) ----------------

// importarPdf extrae texto del PDF y segmenta preguntas candidatas por
// heurística (numeración + marcadores A-D). Los ítems creados quedan en
// 'borrador' con origen 'oficial' y SIN alternativa correcta marcada: el
// validador de publicación (domain.ValidarAlternativas) ya impide
// publicarlos hasta que el admin los revise y complete (RN-04).
func (h *bancoHandler) importarPdf(w http.ResponseWriter, r *http.Request) {
	examenID := chi.URLParam(r, "examenId")
	examen, err := h.examenes.PorID(r.Context(), examenID)
	if errors.Is(err, repo.ErrNoEncontrado) {
		escribirError(w, http.StatusNotFound, "NO_ENCONTRADO", "Examen no encontrado")
		return
	}
	if err != nil {
		escribirError(w, http.StatusInternalServerError, "INTERNO", "Error al obtener el examen")
		return
	}

	r.Body = http.MaxBytesReader(w, r.Body, 20<<20) // 20MB
	if err := r.ParseMultipartForm(20 << 20); err != nil {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Archivo inválido o demasiado grande (máx. 20MB)")
		return
	}

	// eje/dificultad se aplican como valor por defecto a TODOS los ítems
	// extraídos; el admin los ajusta por ítem durante la revisión.
	eje := domain.Eje(r.FormValue("eje"))
	dificultad := domain.Dificultad(r.FormValue("dificultad"))
	if !eje.Valido() || !dificultad.Valido() {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Debe indicar 'eje' y 'dificultad' válidos como valores por defecto para los ítems extraídos")
		return
	}

	file, header, err := r.FormFile("archivo")
	if err != nil {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Falta el archivo 'archivo'")
		return
	}
	defer file.Close()

	texto, err := pdfimport.ExtraerTexto(file, header.Size)
	if err != nil {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "No se pudo leer el PDF (¿está escaneado como imagen o corrupto?)")
		return
	}
	preguntas := pdfimport.SegmentarPreguntas(texto)
	if len(preguntas) == 0 {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "No se detectaron preguntas en el PDF; cárguelas manualmente")
		return
	}

	creados := make([]domain.Item, 0, len(preguntas))
	for _, p := range preguntas {
		alts := make([]domain.Alternativa, 0, len(p.Alternativas))
		for _, a := range p.Alternativas {
			alts = append(alts, domain.Alternativa{
				Etiqueta: domain.EtiquetaAlternativa(a.Etiqueta),
				Texto:    a.Texto,
			})
		}
		it := domain.Item{
			ExamenFuenteID: &examenID,
			Enunciado:      p.Enunciado,
			Eje:            eje,
			Nivel:          examen.Nivel,
			Dificultad:     dificultad,
			Origen:         domain.OrigenOficial,
			Alternativas:   alts,
		}
		creado, err := h.items.Crear(r.Context(), it)
		if err != nil {
			escribirError(w, http.StatusInternalServerError, "INTERNO", "Se detuvo la importación a mitad de camino: no se pudo crear un ítem")
			return
		}
		creados = append(creados, creado)
	}

	escribirJSON(w, http.StatusCreated, creados)
}

// ---------------- Imágenes ----------------

func (h *bancoHandler) subirImagen(w http.ResponseWriter, r *http.Request) {
	r.Body = http.MaxBytesReader(w, r.Body, 5<<20) // 5MB
	if err := r.ParseMultipartForm(5 << 20); err != nil {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Archivo inválido o demasiado grande (máx. 5MB)")
		return
	}
	file, header, err := r.FormFile("archivo")
	if err != nil {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", "Falta el archivo 'archivo'")
		return
	}
	defer file.Close()

	url, err := h.imagenes.Guardar(header.Filename, file)
	if err != nil {
		escribirError(w, http.StatusUnprocessableEntity, "VALIDACION", err.Error())
		return
	}
	escribirJSON(w, http.StatusCreated, map[string]string{"url": url})
}
