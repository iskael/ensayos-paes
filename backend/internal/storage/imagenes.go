package storage

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
)

type Imagenes struct {
	dir     string
	baseURL string
}

func NewImagenes(dir, baseURL string) (*Imagenes, error) {
	if err := os.MkdirAll(dir, 0o755); err != nil {
		return nil, err
	}
	return &Imagenes{dir: dir, baseURL: strings.TrimRight(baseURL, "/")}, nil
}

var extensionesPermitidas = map[string]bool{".png": true, ".jpg": true, ".jpeg": true, ".webp": true}

// Guardar escribe el archivo con un nombre aleatorio (evita colisiones y no
// expone el nombre original) y retorna la URL pública.
func (s *Imagenes) Guardar(nombreOriginal string, r io.Reader) (string, error) {
	ext := strings.ToLower(filepath.Ext(nombreOriginal))
	if !extensionesPermitidas[ext] {
		return "", fmt.Errorf("extensión no permitida: %s", ext)
	}
	nombre, err := nombreAleatorio()
	if err != nil {
		return "", err
	}
	nombre += ext

	destino := filepath.Join(s.dir, nombre)
	f, err := os.Create(destino)
	if err != nil {
		return "", err
	}
	defer f.Close()
	if _, err := io.Copy(f, r); err != nil {
		return "", err
	}
	return s.baseURL + "/" + nombre, nil
}

func nombreAleatorio() (string, error) {
	b := make([]byte, 16)
	if _, err := rand.Read(b); err != nil {
		return "", err
	}
	return hex.EncodeToString(b), nil
}
