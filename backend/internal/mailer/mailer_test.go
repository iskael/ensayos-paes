package mailer

import "strings"

import "testing"

func TestConstruirMensaje(t *testing.T) {
	m := New(Config{
		Usuario:    "cuenta@gmail.com",
		Remitente:  "Ensayos PAES <cuenta@gmail.com>",
		AppBaseURL: "https://ensayos.example.com",
	})
	asunto, cuerpo := m.construirMensajeVerificacion("Ana", "tok123")

	if !strings.Contains(asunto, "Confirma") {
		t.Fatalf("el asunto debería mencionar la confirmación, obtuve: %q", asunto)
	}
	if !strings.Contains(cuerpo, "https://ensayos.example.com/verificar-email?token=tok123") {
		t.Fatalf("el cuerpo debería incluir el link completo con el token, obtuve: %q", cuerpo)
	}
	if !strings.Contains(cuerpo, "Ana") {
		t.Fatalf("el cuerpo debería saludar por nombre, obtuve: %q", cuerpo)
	}
}
