package httpx

import (
	"net"
	"net/http"
	"sync"
	"time"
)

// limitadorTasa es un limitador de ventana fija en memoria, pensado para una
// sola instancia del backend (MVP). Ante múltiples instancias, reemplazar
// por un store compartido (p. ej. Redis).
type limitadorTasa struct {
	mu       sync.Mutex
	intentos map[string][]time.Time
	max      int
	ventana  time.Duration
}

func nuevoLimitadorTasa(max int, ventana time.Duration) *limitadorTasa {
	return &limitadorTasa{intentos: map[string][]time.Time{}, max: max, ventana: ventana}
}

func (l *limitadorTasa) permitir(clave string) bool {
	l.mu.Lock()
	defer l.mu.Unlock()

	ahora := time.Now()
	corte := ahora.Add(-l.ventana)

	vigentes := l.intentos[clave][:0]
	for _, t := range l.intentos[clave] {
		if t.After(corte) {
			vigentes = append(vigentes, t)
		}
	}
	if len(vigentes) >= l.max {
		l.intentos[clave] = vigentes
		return false
	}
	l.intentos[clave] = append(vigentes, ahora)
	return true
}

// LimitarTasa responde 429 si la IP supera el límite configurado en `l`.
func LimitarTasa(l *limitadorTasa) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			if !l.permitir(clienteIP(r)) {
				escribirError(w, http.StatusTooManyRequests, "DEMASIADOS_INTENTOS", "Demasiados intentos, intente de nuevo más tarde")
				return
			}
			next.ServeHTTP(w, r)
		})
	}
}

func clienteIP(r *http.Request) string {
	if xff := r.Header.Get("X-Forwarded-For"); xff != "" {
		return xff
	}
	host, _, err := net.SplitHostPort(r.RemoteAddr)
	if err != nil {
		return r.RemoteAddr
	}
	return host
}
