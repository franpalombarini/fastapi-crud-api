import os
import tempfile

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_crear_cliente():
    r = client.post("/clientes", json={
        "nombre": "Ana García", "email": "ana@example.com",
        "telefono": "261-123456", "empresa": "Distribuidora Sur"
    })
    assert r.status_code == 201
    data = r.json()
    assert data["id"] == 1
    assert data["nombre"] == "Ana García"


def test_email_duplicado():
    r = client.post("/clientes", json={"nombre": "Otro", "email": "ana@example.com"})
    assert r.status_code == 409


def test_listar_y_obtener():
    r = client.get("/clientes")
    assert r.status_code == 200
    assert len(r.json()) == 1
    r = client.get("/clientes/1")
    assert r.status_code == 200
    assert r.json()["email"] == "ana@example.com"


def test_actualizar():
    r = client.put("/clientes/1", json={
        "nombre": "Ana García López", "email": "ana@example.com",
        "empresa": "Distribuidora Sur SRL"
    })
    assert r.status_code == 200
    assert r.json()["nombre"] == "Ana García López"


def test_eliminar_y_404():
    assert client.delete("/clientes/1").status_code == 204
    assert client.get("/clientes/1").status_code == 404
