# FastAPI CRUD API

API REST de ejemplo para gestionar **clientes** de una PyME, construida con FastAPI + SQLite.

Demo de servicio freelance: backend listo para extender (facturación, usuarios, reportes).

## Stack
- FastAPI + Uvicorn
- SQLite (vía sqlite3 stdlib, cero configuración)
- Pydantic para validación
- pytest + httpx para tests

## Uso rápido

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Documentación interactiva en http://127.0.0.1:8000/docs

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /health | Estado del servicio |
| GET | /clientes | Lista todos los clientes |
| GET | /clientes/{id} | Un cliente por id |
| POST | /clientes | Crear cliente |
| PUT | /clientes/{id} | Actualizar cliente |
| DELETE | /clientes/{id} | Eliminar cliente |

## Tests

```bash
pytest -v
```

5 tests: health, crear, listar, actualizar, eliminar (usan base de datos temporal aislada).
