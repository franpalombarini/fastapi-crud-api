from fastapi import FastAPI, HTTPException
import sqlite3

from .database import init_db, get_conn
from .models import ClienteIn, Cliente

app = FastAPI(title="CRUD Clientes - PyME", version="1.0.0")
init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/clientes", response_model=list[Cliente])
def listar():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM clientes ORDER BY id").fetchall()
    return [dict(r) for r in rows]


@app.get("/clientes/{cid}", response_model=Cliente)
def obtener(cid: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM clientes WHERE id=?", (cid,)).fetchone()
    if not row:
        raise HTTPException(404, "Cliente no encontrado")
    return dict(row)


@app.post("/clientes", response_model=Cliente, status_code=201)
def crear(c: ClienteIn):
    try:
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO clientes (nombre, email, telefono, empresa) VALUES (?,?,?,?)",
                (c.nombre, c.email, c.telefono, c.empresa),
            )
            cid = cur.lastrowid
            row = conn.execute("SELECT * FROM clientes WHERE id=?", (cid,)).fetchone()
    except sqlite3.IntegrityError:
        raise HTTPException(409, "Email ya registrado")
    return dict(row)


@app.put("/clientes/{cid}", response_model=Cliente)
def actualizar(cid: int, c: ClienteIn):
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE clientes SET nombre=?, email=?, telefono=?, empresa=? WHERE id=?",
            (c.nombre, c.email, c.telefono, c.empresa, cid),
        )
        if cur.rowcount == 0:
            raise HTTPException(404, "Cliente no encontrado")
        row = conn.execute("SELECT * FROM clientes WHERE id=?", (cid,)).fetchone()
    return dict(row)


@app.delete("/clientes/{cid}", status_code=204)
def eliminar(cid: int):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM clientes WHERE id=?", (cid,))
        if cur.rowcount == 0:
            raise HTTPException(404, "Cliente no encontrado")
