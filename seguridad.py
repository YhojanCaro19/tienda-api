from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Configuracion (en un proyecto real, la clave va en una variable de entorno)
SECRET_KEY = "clave-super-secreta-de-mas-de-32-caracteres-cambieme"
ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 30


# ---------- Hashing de contrasenas (bcrypt) ----------
def hashear_password(password: str) -> str:
    hasheado = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hasheado.decode()


def verificar_password(plano: str, hasheado: str) -> bool:
    return bcrypt.checkpw(plano.encode(), hasheado.encode())


# ---------- Usuarios de prueba (contrasena guardada como hash) ----------
usuarios = [
    {"username": "admin", "nombre": "Administrador",
     "password": hashear_password("admin123"), "rol": "admin"},
    {"username": "ana", "nombre": "Ana Cliente",
     "password": hashear_password("ana123"), "rol": "cliente"},
]


def buscar_usuario(username: str):
    for usuario in usuarios:
        if usuario["username"] == username:
            return usuario
    return None


# ---------- Tokens JWT ----------
def crear_token(username: str) -> str:
    """Crea un token firmado que guarda el usuario (sub) y su expiracion (exp)."""
    expira = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    return jwt.encode({"sub": username, "exp": expira}, SECRET_KEY, algorithm=ALGORITMO)


# Le dice a FastAPI donde se obtiene el token (activa el boton Authorize en /docs)
oauth2_esquema = OAuth2PasswordBearer(tokenUrl="auth/login")


# ---------- Dependencias ----------
def obtener_usuario_actual(token: str = Depends(oauth2_esquema)):
    """Valida el token y devuelve el usuario. Si falla -> 401."""
    error = HTTPException(status_code=401, detail="Token invalido",
                          headers={"WWW-Authenticate": "Bearer"})
    try:
        datos = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
        username = datos.get("sub")
        if username is None:
            raise error
    except jwt.PyJWTError:
        raise error
    usuario = buscar_usuario(username)
    if usuario is None:
        raise error
    return usuario


def requerir_admin(usuario: dict = Depends(obtener_usuario_actual)):
    """Exige rol admin. Si el usuario no lo es -> 403."""
    if usuario["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Requiere rol de administrador")
    return usuario
