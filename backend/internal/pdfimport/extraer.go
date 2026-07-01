package pdfimport

import (
	"io"
	"strings"

	"github.com/ledongthuc/pdf"
)

// ExtraerTexto obtiene el texto plano de un PDF. r debe soportar lectura
// aleatoria (multipart.File ya lo hace) y se necesita el tamaño en bytes.
// Páginas no extraíbles (p. ej. escaneadas como imagen) se omiten en
// silencio; si ninguna página produce texto, el resultado es "" y la
// segmentación posterior simplemente no encontrará preguntas.
func ExtraerTexto(r io.ReaderAt, size int64) (string, error) {
	doc, err := pdf.NewReader(r, size)
	if err != nil {
		return "", err
	}

	var sb strings.Builder
	total := doc.NumPage()
	for i := 1; i <= total; i++ {
		page := doc.Page(i)
		if page.V.IsNull() {
			continue
		}
		texto, err := page.GetPlainText(nil)
		if err != nil {
			continue
		}
		sb.WriteString(texto)
		sb.WriteString("\n")
	}
	return sb.String(), nil
}
