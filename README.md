# API de la Tienda — FastAPI con seguridad (OAuth2 + JWT + roles)

API REST para una tienda de comercio electrónico construida con **FastAPI**. Sobre el CRUD de la Guía 2 se agregó **seguridad**: contraseñas guardadas con **bcrypt**, inicio de sesión con **OAuth2** que entrega un **token JWT**, endpoints protegidos con **`Depends`** y **autorización por roles** (`admin` y `cliente`).
Evidencias **GA3-AA2-EV03** y **GA3-AA3-EV04** de la Guía 3 (ADSO 228118 – SENA).

**Equipo:** Yhojan Caro · Sebastian Gonzalez · Emannuel Castaño Espinoza — Ficha 3229209

Los datos siguen en memoria (listas de Python), por eso se reinician cada vez que se detiene el servidor.

## Reglas de seguridad

| Operación | Quién puede | Si no cumple |
|-----------|-------------|--------------|
| `GET` (listar y obtener uno) | Cualquiera, sin iniciar sesión | — |
| `POST` y `PUT` | Cualquier usuario autenticado (token válido) | **401 Unauthorized** |
| `DELETE` | Solo usuarios con rol `admin` | **401** sin token · **403 Forbidden** si es `cliente` |

Las mismas reglas se aplican a los **cuatro recursos**: productos, categorías, proveedores y pedidos.

- **Autenticación** (¿quién eres?) → `obtener_usuario_actual` valida el token. Si falta, está vencido o fue alterado → 401.
- **Autorización** (¿qué puedes hacer?) → `requerir_admin` revisa el rol. Si no es admin → 403.

## Estructura del proyecto

```
tienda-api/
|-- main.py              # crea la app e incluye los routers
|-- seguridad.py         # hashing bcrypt, usuarios, crear_token y dependencias (401 / 403)
|-- routers/
|   |-- __init__.py
|   |-- auth.py          # POST /auth/login, POST /auth/registro, GET /auth/yo
|   |-- productos.py     # CRUD de productos protegido
|   |-- categorias.py    # CRUD de categorías protegido (reto)
|   |-- proveedores.py   # recurso extra 1, protegido
|   |-- pedidos.py       # recurso extra 2, protegido
|-- requirements.txt
|-- README.md
|-- .gitignore
`-- capturas/            # pruebas en /docs (Authorize + Try it out -> Execute)
```

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| `admin` | `admin123` | admin |
| `ana` | `ana123` | cliente |

Las contraseñas **no** se guardan en texto plano: en `seguridad.py` se guarda el hash bcrypt (`$2b$12$...`). También se pueden crear usuarios nuevos con `POST /auth/registro` (siempre quedan con rol `cliente`).

## Endpoints

### Autenticación (`routers/auth.py`)

| Método | Ruta | Descripción | Protección | Éxito | Errores |
|--------|------|-------------|------------|-------|---------|
| POST | `/auth/login` | Recibe usuario y contraseña (formulario) y devuelve el token | Pública | 200 | 401, 422 |
| POST | `/auth/registro` | Crea un usuario con rol cliente y contraseña hasheada | Pública | **201** | 400 (ya existe), 422 |
| GET | `/auth/yo` | Devuelve el dueño del token | Token | 200 | 401 |

Respuesta del login:

```json
{ "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "token_type": "bearer" }
```

### Productos, categorías, proveedores y pedidos

| Método | Ruta | Protección | Éxito | Errores |
|--------|------|------------|-------|---------|
| GET | `/productos` · `/categorias` · `/proveedores` · `/pedidos` | Pública | 200 | — |
| GET | `/{recurso}/{id}` | Pública | 200 | 404, 422 |
| POST | `/{recurso}` | Token | **201** | 401, 422 |
| PUT | `/{recurso}/{id}` | Token | 200 | 401, 404, 422 |
| DELETE | `/{recurso}/{id}` | Rol admin | 200 | 401, 403, 404 |

Cuerpos (JSON) para POST y PUT:

```json
// productos
{ "nombre": "Mouse gamer", "precio": 85000, "categoria": "Perifericos" }
// categorias
{ "nombre": "Almacenamiento" }
// proveedores
{ "nombre": "Importadora del Valle", "telefono": "3205551234", "ciudad": "Cali" }
// pedidos (el cliente se toma del token, no del body)
{ "producto_id": 3, "cantidad": 2 }
```

Las respuestas de POST, PUT y DELETE indican quién hizo la operación (`creado_por`, `actualizado_por`, `eliminado_por`).

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/YhojanCaro19/tienda-api.git
cd tienda-api

# 2. Crear el entorno virtual
python -m venv venv

# 3. Activarlo
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS

# 4. Instalar dependencias (FastAPI, Uvicorn, PyJWT, bcrypt, python-multipart)
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs (botón **Authorize** y candado en los endpoints protegidos)

## Cómo probar la seguridad en /docs

1. Pulse **Authorize**, escriba `admin` / `admin123` y confirme.
2. `POST /productos` → **201** y la respuesta muestra `"creado_por": "admin"`.
3. **Logout**, vuelva a **Authorize** como `ana` / `ana123` e intente `DELETE /productos/1` → **403**.
4. Sin sesión (Logout), intente `POST /productos` → **401**.

Con curl:

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/auth/login \
  -d "username=admin&password=admin123" | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

curl -X DELETE http://127.0.0.1:8000/categorias/1 -H "Authorization: Bearer $TOKEN"
```

## Capturas de pantalla

Todas las pruebas se hicieron desde `/docs` sobre el mismo servidor. Están en [`capturas/`](capturas/) (las de la Guía 2 quedaron en `capturas/guia2/`).

### Práctica guiada (productos + autenticación)

| Captura | Qué muestra |
|---------|-------------|
| `00_docs_general.png` | Swagger con el botón **Authorize** y candados en los endpoints protegidos |
| `01_authorize_admin.png` | Ventana Authorize con `admin` / `admin123` |
| `02_authorize_admin_ok.png` | Sesión iniciada como admin (Authorized) |
| `03_productos_post_admin_201.png` | `POST /productos` como admin → **201**, `creado_por: admin` |
| `04_auth_yo_admin.png` | `GET /auth/yo` → usuario admin, rol admin |
| `05_productos_post_ana_201.png` | Ejercicio 1: `POST /productos` como ana → **201**, `creado_por: ana` |
| `06_productos_delete_ana_403.png` | Ejercicio 2: ana intenta `DELETE /productos/1` → **403** |
| `07_productos_post_sin_token_401.png` | Ejercicio 2: `POST /productos` sin token → **401** |
| `08_login_fallido_401.png` | Ejercicio 2: login con contraseña incorrecta → **401** |
| `09_registro_201.png` | Ejercicio 3: `POST /auth/registro` (carlos) → **201**, rol cliente |
| `10_login_carlos_200.png` | Ejercicio 3: login con el usuario nuevo → token |
| `11_auth_yo_carlos.png` | Ejercicio 3: `GET /auth/yo` con el token de carlos |
| `12_productos_put_sin_token_401.png` | Ejercicio 4: `PUT /productos/2` sin token → **401** |
| `13_productos_put_carlos_200.png` | Ejercicio 4: `PUT /productos/2` autenticado → **200** |
| `14_productos_get_publico_200.png` | `GET /productos` sin sesión → **200** (sigue público) |
| `15_productos_delete_admin_200.png` | `DELETE /productos/1` como admin → **200** |

### Reto: categorías, proveedores y pedidos

Para cada recurso (`categorias_`, `proveedores_`, `pedidos_`) hay 9 capturas:

| Sufijo | Qué muestra |
|--------|-------------|
| `01_get_publico_200` | GET de la lista sin sesión → **200** |
| `02_post_sin_token_401` | POST sin token → **401** |
| `03_put_sin_token_401` | PUT sin token → **401** |
| `04_delete_sin_token_401` | DELETE sin token → **401** |
| `05_post_ana_201` | POST como ana (cliente) → **201** |
| `06_put_ana_200` | PUT como ana → **200** |
| `07_delete_ana_403` | DELETE como ana → **403** |
| `08_delete_admin_200` | DELETE como admin → **200** |
| `09_get_final` | GET con los cambios aplicados |

## Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/) — framework web y sistema de dependencias (`Depends`)
- [PyJWT](https://pyjwt.readthedocs.io/) — creación y validación de tokens JWT (HS256, 30 min)
- [bcrypt](https://pypi.org/project/bcrypt/) — hashing de contraseñas
- [python-multipart](https://pypi.org/project/python-multipart/) — formulario del login
- [Uvicorn](https://www.uvicorn.org/) — servidor ASGI

> Nota: la `SECRET_KEY` está en el código solo con fines de aprendizaje; en un proyecto real va en una variable de entorno.
