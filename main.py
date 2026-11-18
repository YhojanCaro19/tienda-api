from fastapi import FastAPI

from routers import auth, categorias, pedidos, productos, proveedores

app = FastAPI(title="API de la Tienda")

# Conectamos los routers de cada recurso
app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(proveedores.router)
app.include_router(pedidos.router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API de la Tienda funcionando. Visita /docs"}
