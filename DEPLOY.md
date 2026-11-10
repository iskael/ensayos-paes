# Despliegue — Proxmox (CT)

Stack completo (Postgres + migraciones + API + frontend) vía `docker-compose.yml`.

## Instancia actual

- **Proxmox host**: `192.168.0.155` (nodo `pve`).
- **CT**: VMID `118`, hostname `ensayos-paes`, IP por DHCP desde 2026-11-09 (`192.168.0.237` a esa fecha; antes fija `192.168.0.190`).
- **App**: frontend en `http://<ip-del-ct>/`, API en `http://<ip-del-ct>:8080`.
- Si la IP cambia hay que actualizar `CORS_ALLOWED_ORIGIN` y `UPLOADS_URL` en `.env` y recrear `api`
  (`docker compose up -d api`): el navegador llama a la API en otro puerto, así que el origen del
  frontend tiene que estar en la lista de CORS.
- Código desplegado copiando el working tree (el repo de GitHub es privado;
  no se pudo `git clone` sin credenciales dentro del CT). Para actualizar,
  repetir la transferencia o configurar un deploy key/PAT y clonar en
  `/opt/app`.

## 1. Contenedor (LXC)

CT Debian 13, sin privilegios, con `nesting=1,keyctl=1` (requerido para correr
Docker dentro del CT), Docker Engine + plugin `compose` instalados desde el
repo oficial de Docker.

## 2. Variables de entorno

En el servidor, crear `.env` (no se commitea) junto a `docker-compose.yml`,
basado en `.env.example`, con al menos:

- `JWT_SECRET` — secreto real, no el de ejemplo.
- `CORS_ALLOWED_ORIGIN` — dominio/IP real del frontend.
- `UPLOADS_URL` — IP/dominio real donde queda expuesta la API.
- `POSTGRES_PASSWORD` — password real, no el de ejemplo.

## 3. Levantar

```bash
docker compose up -d --build
```

Orden de arranque: `db` (con healthcheck) → `migrate` (aplica
`backend/migrations`, corre una vez y termina) → `api` (espera a que
`migrate` termine con éxito) → `web`.

## 4. Primer administrador

El registro público no permite rol admin (ver `backend/README.md`). Crearlo
con el binario `seed-admin` empaquetado en la imagen de `api`:

```bash
docker compose exec api ./seed-admin -email=admin@tudominio.cl -password=UnaClaveSegura123
```

## 5. Puertos

- `80` — frontend (nginx, estático). `frontend/nginx.conf` devuelve `index.html` para las rutas de
  la SPA (`/login`, `/dashboard`, …), de modo que entrar directo o recargar no da 404.
- `8080` — API (`/api/v1/*`, `/uploads/*`, `/health`).
- `5432` — Postgres (expuesto para debugging; considerar cerrarlo en el
  firewall del CT si no se necesita acceso externo).
