from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import seguridad

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


class ProveedorEntrada(BaseModel):
    nombre: str
    telefono: str
    ciudad: str


proveedores = [
    {"id": 1, "nombre": "TecnoImport SAS", "telefono": "3001234567", "ciudad": "Medellin"},
    {"id": 2, "nombre": "Distribuidora Andina", "telefono": "3109876543", "ciudad": "Bogota"},
]


# LISTAR (publico)                   GET /proveedores
@router.get("")
def listar_proveedores():
    return proveedores


# OBTENER UNO (publico)              GET /proveedores/{proveedor_id}
@router.get("/{proveedor_id}")
def obtener_proveedor(proveedor_id: int):
    for proveedor in proveedores:
        if proveedor["id"] == proveedor_id:
            return proveedor
    raise HTTPException(status_code=404, detail="Proveedor no encontrado")


# CREAR (requiere token)             POST /proveedores
@router.post("", status_code=201)
def crear_proveedor(datos: ProveedorEntrada,
                    usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    nuevo_id = max((p["id"] for p in proveedores), default=0) + 1
    nuevo = {"id": nuevo_id, **datos.model_dump()}
    proveedores.append(nuevo)
    return {"mensaje": "Proveedor creado", "proveedor": nuevo,
            "creado_por": usuario["username"]}


# ACTUALIZAR (requiere token)        PUT /proveedores/{proveedor_id}
@router.put("/{proveedor_id}")
def actualizar_proveedor(proveedor_id: int, datos: ProveedorEntrada,
                         usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    for proveedor in proveedores:
        if proveedor["id"] == proveedor_id:
            proveedor.update(datos.model_dump())
            return {"mensaje": "Proveedor actualizado", "proveedor": proveedor,
                    "actualizado_por": usuario["username"]}
    raise HTTPException(status_code=404, detail="Proveedor no encontrado")


# ELIMINAR (solo admin)              DELETE /proveedores/{proveedor_id}
@router.delete("/{proveedor_id}")
def eliminar_proveedor(proveedor_id: int,
                       admin: dict = Depends(seguridad.requerir_admin)):
    for proveedor in proveedores:
        if proveedor["id"] == proveedor_id:
            proveedores.remove(proveedor)
            return {"mensaje": "Proveedor eliminado", "proveedor": proveedor,
                    "eliminado_por": admin["username"]}
    raise HTTPException(status_code=404, detail="Proveedor no encontrado")
