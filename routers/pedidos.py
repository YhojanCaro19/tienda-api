from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

import seguridad

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


class PedidoEntrada(BaseModel):
    producto_id: int
    cantidad: int = Field(gt=0)


pedidos = [
    {"id": 1, "cliente": "ana", "producto_id": 2, "cantidad": 1, "estado": "pendiente"},
]


# LISTAR (publico)                   GET /pedidos
@router.get("")
def listar_pedidos():
    return pedidos


# OBTENER UNO (publico)              GET /pedidos/{pedido_id}
@router.get("/{pedido_id}")
def obtener_pedido(pedido_id: int):
    for pedido in pedidos:
        if pedido["id"] == pedido_id:
            return pedido
    raise HTTPException(status_code=404, detail="Pedido no encontrado")


# CREAR (requiere token)             POST /pedidos
# El cliente del pedido se toma del token, no del body: nadie puede pedir a nombre de otro.
@router.post("", status_code=201)
def crear_pedido(datos: PedidoEntrada,
                 usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    nuevo_id = max((p["id"] for p in pedidos), default=0) + 1
    nuevo = {"id": nuevo_id, "cliente": usuario["username"],
             "producto_id": datos.producto_id, "cantidad": datos.cantidad,
             "estado": "pendiente"}
    pedidos.append(nuevo)
    return {"mensaje": "Pedido creado", "pedido": nuevo,
            "creado_por": usuario["username"]}


# ACTUALIZAR (requiere token)        PUT /pedidos/{pedido_id}
@router.put("/{pedido_id}")
def actualizar_pedido(pedido_id: int, datos: PedidoEntrada,
                      usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    for pedido in pedidos:
        if pedido["id"] == pedido_id:
            pedido["producto_id"] = datos.producto_id
            pedido["cantidad"] = datos.cantidad
            return {"mensaje": "Pedido actualizado", "pedido": pedido,
                    "actualizado_por": usuario["username"]}
    raise HTTPException(status_code=404, detail="Pedido no encontrado")


# ELIMINAR (solo admin)              DELETE /pedidos/{pedido_id}
@router.delete("/{pedido_id}")
def eliminar_pedido(pedido_id: int,
                    admin: dict = Depends(seguridad.requerir_admin)):
    for pedido in pedidos:
        if pedido["id"] == pedido_id:
            pedidos.remove(pedido)
            return {"mensaje": "Pedido eliminado", "pedido": pedido,
                    "eliminado_por": admin["username"]}
    raise HTTPException(status_code=404, detail="Pedido no encontrado")
