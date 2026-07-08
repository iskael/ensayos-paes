// Package mailer envía correos por SMTP (pensado para una cuenta de Gmail
// con contraseña de aplicación). Solo internal/http/auth_handler.go lo usa.
package mailer

import (
	"fmt"
	"net/smtp"
)

type Config struct {
	Host       string
	Port       string
	Usuario    string
	Password   string
	Remitente  string
	AppBaseURL string
}

type Mailer struct {
	cfg Config
}

func New(cfg Config) *Mailer {
	return &Mailer{cfg: cfg}
}

// construirMensajeVerificacion arma el asunto y el cuerpo del correo, sin
// tocar la red — separado de EnviarVerificacion para poder testearlo sin
// credenciales SMTP reales.
func (m *Mailer) construirMensajeVerificacion(nombre, token string) (asunto, cuerpo string) {
	link := fmt.Sprintf("%s/verificar-email?token=%s", m.cfg.AppBaseURL, token)
	asunto = "Confirma tu cuenta - Ensayos PAES"
	cuerpo = fmt.Sprintf(
		"Hola %s,\n\nConfirma tu cuenta haciendo clic en este link:\n%s\n\nEste link expira en 24 horas. Si no creaste esta cuenta, ignora este mensaje.",
		nombre, link,
	)
	return asunto, cuerpo
}

// EnviarVerificacion manda el correo de verificación. Un error acá NO debe
// hacer fallar el registro del usuario que lo llama — solo se loguea.
func (m *Mailer) EnviarVerificacion(destinatario, nombre, token string) error {
	asunto, cuerpo := m.construirMensajeVerificacion(nombre, token)
	mensaje := []byte(fmt.Sprintf("To: %s\r\nSubject: %s\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n%s\r\n", destinatario, asunto, cuerpo))

	auth := smtp.PlainAuth("", m.cfg.Usuario, m.cfg.Password, m.cfg.Host)
	addr := fmt.Sprintf("%s:%s", m.cfg.Host, m.cfg.Port)
	return smtp.SendMail(addr, auth, m.cfg.Remitente, []string{destinatario}, mensaje)
}
