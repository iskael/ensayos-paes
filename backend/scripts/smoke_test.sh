#!/usr/bin/env bash
# Smoke test end-to-end del MVP Ensayos PAES.
# Requiere: curl, jq. Requiere el servidor corriendo (go run ./cmd/api) y un
# admin ya creado (ver cmd/seed-admin).
#
# Uso:
#   ./scripts/smoke_test.sh <admin_email> <admin_password>
set -euo pipefail

command -v jq >/dev/null || { echo "Este script necesita 'jq' instalado (apt install jq / brew install jq)."; exit 1; }

BASE_URL="${BASE_URL:-http://localhost:8080}"
API="$BASE_URL/api/v1"
ADMIN_EMAIL="${1:?uso: $0 <admin_email> <admin_password>}"
ADMIN_PASSWORD="${2:?uso: $0 <admin_email> <admin_password>}"
SUFIJO=$RANDOM

paso() { echo; echo "== $1 =="; }
ok()   { echo "  ✓ $1"; }
fail() { echo "  ✗ $1"; exit 1; }

# llamar METODO URL [BODY] [TOKEN]  -> deja la respuesta en RESP_BODY / RESP_STATUS
llamar() {
  local metodo="$1" url="$2" body="${3:-}" token="${4:-}"
  local args=(-s -w '\n%{http_code}' -X "$metodo" "$url" -H "Content-Type: application/json")
  [ -n "$token" ] && args+=(-H "Authorization: Bearer $token")
  [ -n "$body" ] && args+=(-d "$body")
  local salida
  salida="$(curl "${args[@]}")"
  RESP_STATUS="${salida##*$'\n'}"
  RESP_BODY="${salida%$'\n'*}"
}

exigir_status() {
  local esperado="$1" contexto="$2"
  if [ "$RESP_STATUS" != "$esperado" ]; then
    echo "  Respuesta: $RESP_BODY"
    fail "$contexto (esperaba HTTP $esperado, obtuve $RESP_STATUS)"
  fi
  ok "$contexto (HTTP $RESP_STATUS)"
}

# ---------- 1. Salud ----------
paso "1. Health check"
llamar GET "$BASE_URL/health"
exigir_status 200 "servidor responde"

# ---------- 2. Registro debe rechazar sin aceptar T&C ----------
paso "2. Registro sin acepta_terminos debe fallar (422)"
llamar POST "$API/auth/register" "{\"nombre\":\"Sin Terminos\",\"email\":\"sinterminos$SUFIJO@test.cl\",\"password\":\"claveClave123\",\"rol\":\"estudiante\",\"acepta_terminos\":false}"
exigir_status 422 "rechaza registro sin aceptar T&C"

# ---------- 3. Registrar profesor y estudiante ----------
paso "3. Registrar profesor y estudiante"
PROF_EMAIL="profesor$SUFIJO@test.cl"
EST_EMAIL="estudiante$SUFIJO@test.cl"

llamar POST "$API/auth/register" "{\"nombre\":\"Profesor Demo\",\"email\":\"$PROF_EMAIL\",\"password\":\"claveClave123\",\"rol\":\"profesor\",\"acepta_terminos\":true}"
exigir_status 201 "profesor registrado"
PROF_TOKEN=$(echo "$RESP_BODY" | jq -r .token)

llamar POST "$API/auth/register" "{\"nombre\":\"Estudiante Demo\",\"email\":\"$EST_EMAIL\",\"password\":\"claveClave123\",\"rol\":\"estudiante\",\"acepta_terminos\":true}"
exigir_status 201 "estudiante registrado"
EST_TOKEN=$(echo "$RESP_BODY" | jq -r .token)

# ---------- 4. Login admin ----------
paso "4. Login admin"
llamar POST "$API/auth/login" "{\"email\":\"$ADMIN_EMAIL\",\"password\":\"$ADMIN_PASSWORD\"}"
exigir_status 200 "login admin"
ADMIN_TOKEN=$(echo "$RESP_BODY" | jq -r .token)

# ---------- 5. Crear examen fuente ----------
paso "5. Crear examen fuente"
llamar POST "$API/examenes" "{\"nombre\":\"Examen Demo Smoke Test\",\"anio_admision\":2026,\"tipo\":\"PAES_Regular\",\"nivel\":\"M1\"}" "$ADMIN_TOKEN"
exigir_status 201 "examen creado"
EXAMEN_ID=$(echo "$RESP_BODY" | jq -r .id)

# ---------- 6. Crear 10 ítems (eje numeros, M1) ----------
paso "6. Crear 10 ítems (eje numeros, M1) con 4 alternativas cada uno"
ITEM_IDS=()
for i in $(seq 1 10); do
  BODY=$(cat <<JSON
{
  "examen_fuente_id": "$EXAMEN_ID",
  "enunciado": "Pregunta de prueba número $i",
  "eje": "numeros",
  "nivel": "M1",
  "dificultad": "media",
  "alternativas": [
    {"etiqueta":"A","texto":"Opción A","es_correcta": true},
    {"etiqueta":"B","texto":"Opción B","es_correcta": false},
    {"etiqueta":"C","texto":"Opción C","es_correcta": false},
    {"etiqueta":"D","texto":"Opción D","es_correcta": false}
  ]
}
JSON
)
  llamar POST "$API/items" "$BODY" "$ADMIN_TOKEN"
  exigir_status 201 "ítem $i creado"
  ITEM_IDS+=("$(echo "$RESP_BODY" | jq -r .id)")
done

# ---------- 7. Definir clave (10 x 100 = 1000) ----------
paso "7. Definir clave del examen (10 ítems x 100 = 1000)"
PESOS_JSON=$(printf '%s\n' "${ITEM_IDS[@]}" | jq -R -s 'split("\n") | map(select(length > 0)) | map({item_id: ., peso: 100})')
llamar PUT "$API/examenes/$EXAMEN_ID/clave" "{\"pesos\": $PESOS_JSON}" "$ADMIN_TOKEN"
exigir_status 200 "clave definida"

# ---------- 8. Publicar los 10 ítems ----------
paso "8. Publicar los 10 ítems"
for id in "${ITEM_IDS[@]}"; do
  llamar POST "$API/items/$id/publicar" "" "$ADMIN_TOKEN"
  exigir_status 200 "ítem $id publicado"
done

# ---------- 9. Estudiante genera un ensayo ----------
paso "9. Estudiante genera un ensayo de 10 preguntas (eje numeros, M1)"
llamar POST "$API/ensayos" "{\"nivel\":\"M1\",\"ejes\":[\"numeros\"],\"cantidad\":10}" "$EST_TOKEN"
exigir_status 201 "ensayo generado"
ENSAYO_ID=$(echo "$RESP_BODY" | jq -r .id)
CANT_PREGUNTAS=$(echo "$RESP_BODY" | jq '.preguntas | length')
echo "  preguntas en el ensayo: $CANT_PREGUNTAS (debería ser 10)"

# ---------- 10. Responder todas con "A" (la marcada como correcta) ----------
paso "10. Guardar respuestas (todas 'A')"
RESPUESTAS_JSON=$(echo "$RESP_BODY" | jq '[.preguntas[] | {ensayo_item_id: .ensayo_item_id, respuesta_seleccionada: "A"}]')
llamar PATCH "$API/ensayos/$ENSAYO_ID/respuestas" "{\"respuestas\": $RESPUESTAS_JSON}" "$EST_TOKEN"
exigir_status 204 "respuestas guardadas"

# ---------- 11. Enviar y corregir ----------
paso "11. Enviar el ensayo (corrige y calcula puntaje)"
llamar POST "$API/ensayos/$ENSAYO_ID/enviar" "" "$EST_TOKEN"
exigir_status 200 "ensayo corregido"
PUNTAJE=$(echo "$RESP_BODY" | jq .puntaje)
echo "  puntaje obtenido: $PUNTAJE / 1000 (esperado 1000: todas las respuestas 'A' eran la correcta)"

# ---------- 12. Consultar resultado ----------
paso "12. Consultar resultado con revisión y desglose por eje"
llamar GET "$API/ensayos/$ENSAYO_ID/resultado" "" "$EST_TOKEN"
exigir_status 200 "resultado obtenido"

# ---------- 13. Dashboard del estudiante ----------
paso "13. Dashboard del estudiante"
llamar GET "$API/dashboard/resumen" "" "$EST_TOKEN"
exigir_status 200 "resumen del dashboard"
echo "$RESP_BODY" | jq .

llamar GET "$API/dashboard/evolucion" "" "$EST_TOKEN"
exigir_status 200 "evolución del dashboard"

# ---------- 14. Grupos: crear, unirse, consultar ----------
paso "14. Profesor crea un grupo"
llamar POST "$API/grupos" "{\"nombre\":\"Curso Demo $SUFIJO\"}" "$PROF_TOKEN"
exigir_status 201 "grupo creado"
CODIGO=$(echo "$RESP_BODY" | jq -r .codigo_invitacion)
GRUPO_ID=$(echo "$RESP_BODY" | jq -r .id)
echo "  código de invitación: $CODIGO"

paso "15. Estudiante se une al grupo"
llamar POST "$API/grupos/unirse" "{\"codigo\":\"$CODIGO\"}" "$EST_TOKEN"
exigir_status 200 "estudiante unido al grupo"

paso "16. Profesor consulta el grupo (detalle y miembros)"
llamar GET "$API/grupos/$GRUPO_ID" "" "$PROF_TOKEN"
exigir_status 200 "detalle del grupo"
echo "$RESP_BODY" | jq .

llamar GET "$API/grupos/$GRUPO_ID/miembros" "" "$PROF_TOKEN"
exigir_status 200 "miembros del grupo"
echo "$RESP_BODY" | jq .

echo
echo "=========================================="
echo " Smoke test completo. Revisa los detalles arriba."
echo "=========================================="
