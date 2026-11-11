# API de la Tienda — FastAPI

API REST para una tienda de comercio electrónico con **CRUD completo** de productos y categorías, construida con **FastAPI**, **Pydantic** y **Uvicorn**.
Evidencias **GA2-AA2-EV03** y **GA2-AA3-EV04** de la Guía 2 (ADSO 228118 – SENA).

**Equipo:** Yhojan Caro · Sebastian Gonzalez · Emanuel Castaño

El proyecto está organizado en varios archivos: cada recurso tiene su propio `APIRouter` dentro de la carpeta `routers/` y `main.py` solo crea la app y conecta los routers. Los datos se guardan en listas en memoria (todavía no usamos base de datos), por eso se reinician cada vez que se detiene el servidor.

## Estructura del proyecto

```
tienda-api/
|-- main.py              # crea la app e incluye los routers
|-- routers/
|   |-- __init__.py      # marca la carpeta como paquete de Python
|   |-- productos.py     # modelo ProductoEntrada + CRUD de productos
|   |-- categorias.py    # modelo CategoriaEntrada + CRUD de categorías
|-- requirements.txt
|-- README.md
|-- .gitignore
`-- capturas/            # pruebas en /docs (Try it out -> Execute)
```

## Endpoints

### Productos (`routers/productos.py`)

| Método | Ruta | Descripción | Código éxito | Errores |
|--------|------|-------------|--------------|---------|
| GET | `/productos` | Lista todos los productos | 200 | — |
| GET | `/productos/{producto_id}` | Obtiene un producto | 200 | 404, 422 |
| POST | `/productos` | Crea un producto | **201** | 422 |
| PUT | `/productos/{producto_id}` | Actualiza un producto | 200 | 404, 422 |
| DELETE | `/productos/{producto_id}` | Elimina un producto | 200 | 404, 422 |

Cuerpo (JSON) para POST y PUT:

```json
{ "nombre": "Mouse gamer", "precio": 85000, "categoria": "Perifericos" }
```

### Categorías (`routers/categorias.py`)

| Método | Ruta | Descripción | Código éxito | Errores |
|--------|------|-------------|--------------|---------|
| GET | `/categorias` | Lista todas las categorías | 200 | — |
| GET | `/categorias/{categoria_id}` | Obtiene una categoría | 200 | 404, 422 |
| POST | `/categorias` | Crea una categoría | **201** | 422 |
| PUT | `/categorias/{categoria_id}` | Actualiza el nombre | 200 | 404, 422 |
| DELETE | `/categorias/{categoria_id}` | Elimina una categoría | 200 | 404, 422 |

Cuerpo (JSON) para POST y PUT:

```json
{ "nombre": "Almacenamiento" }
```

- **404 Not Found:** el id no existe → `{"detail": "Categoria no encontrada"}`.
- **422 Unprocessable Content:** falta un campo obligatorio o el tipo es incorrecto (por ejemplo, el precio llega como texto). La validación la hace Pydantic de forma automática.

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

# 4. Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn main:app --reload
```

La API queda disponible en http://127.0.0.1:8000

- Documentación interactiva (Swagger UI): http://127.0.0.1:8000/docs
- Documentación de lectura (ReDoc): http://127.0.0.1:8000/redoc

## Ejemplos

```
POST http://127.0.0.1:8000/categorias      body: {"nombre": "Almacenamiento"}
→ 201 {"mensaje": "Categoria creada", "categoria": {"id": 4, "nombre": "Almacenamiento"}}

PUT http://127.0.0.1:8000/categorias/3     body: {"nombre": "Audio y sonido"}
→ 200 {"mensaje": "Categoria actualizada", "categoria": {"id": 3, "nombre": "Audio y sonido"}}

GET http://127.0.0.1:8000/categorias/99
→ 404 {"detail": "Categoria no encontrada"}

POST http://127.0.0.1:8000/productos       body: {"nombre": "Webcam HD", "precio": "caro", "categoria": "Perifericos"}
→ 422 {"detail": [{"type": "float_parsing", "loc": ["body", "precio"], ...}]}
```

## Capturas de pantalla

Cada operación se probó desde `/docs` con **Try it out → Execute**, en orden y sobre el mismo servidor. Las capturas están en [`capturas/`](capturas/):

| Captura | Qué muestra |
|---------|-------------|
| `00_docs_general.png` | Swagger UI con los endpoints agrupados por tags (Productos, Categorias, Inicio) |
| `categorias_01_get_listar.png` | `GET /categorias` → 200 |
| `categorias_02_get_obtener.png` | `GET /categorias/2` → 200 |
| `categorias_03_post_crear_201.png` | `POST /categorias` con `{"nombre": "Almacenamiento"}` → **201** |
| `categorias_04_put_actualizar.png` | `PUT /categorias/3` con `{"nombre": "Audio y sonido"}` → 200 |
| `categorias_05_delete_eliminar.png` | `DELETE /categorias/4` → 200 |
| `categorias_06_get_listar_final.png` | `GET /categorias` con los cambios aplicados |
| `categorias_07_get_404.png` | `GET /categorias/99` → **404** |
| `categorias_08_put_404.png` | `PUT /categorias/99` → **404** |
| `categorias_09_delete_404.png` | `DELETE /categorias/99` → **404** |
| `categorias_10_post_422.png` | `POST /categorias` sin el campo `nombre` → **422** |
| `productos_01_post_crear_201.png` | `POST /productos` (Audifonos inalambricos) → 201 |
| `productos_02_post_crear_201.png` | `POST /productos` (Disco SSD 1TB) → 201 |
| `productos_03_get_listar.png` | `GET /productos` con los dos productos nuevos |
| `productos_04_put_actualizar.png` | `PUT /productos/2` cambia el precio a 79000 |
| `productos_05_get_obtener.png` | `GET /productos/2` confirma el nuevo precio |
| `productos_06_delete_eliminar.png` | `DELETE /productos/3` → 200 |
| `productos_07_get_listar_sin_eliminado.png` | `GET /productos` ya sin el producto 3 |
| `productos_08_get_404.png` | `GET /productos/99` → **404** |
| `productos_09_post_422.png` | `POST /productos` con `"precio": "caro"` → **422** |

## Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/) — framework web
- [Pydantic](https://docs.pydantic.dev/) — modelos y validación de datos (`BaseModel`)
- [Uvicorn](https://www.uvicorn.org/) — servidor ASGI
