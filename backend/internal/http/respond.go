package httpx

import (
	"encoding/json"
	"net/http"
)

type ErrorResp struct {
	Codigo  string `json:"codigo"`
	Mensaje string `json:"mensaje"`
}

func escribirJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func escribirError(w http.ResponseWriter, status int, codigo, mensaje string) {
	escribirJSON(w, status, ErrorResp{Codigo: codigo, Mensaje: mensaje})
}
