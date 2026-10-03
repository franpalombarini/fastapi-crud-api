from pydantic import BaseModel, EmailStr


class ClienteIn(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str | None = None
    empresa: str | None = None


class Cliente(ClienteIn):
    id: int
