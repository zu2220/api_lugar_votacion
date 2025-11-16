from datetime import date
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import json
import os

app = FastAPI(title="ONPE Mock API")


class ConsultaRequest(BaseModel):
    dni: str = Field(..., description="DNI (8 dígitos)")
    fecha_emision: date = Field(..., description="Fecha de emisión del DNI (YYYY-MM-DD)")
    digito_verificador: str = Field(..., description="Dígito verificador del DNI (un dígito)")


class Lugar(BaseModel):
    nombre: str
    lat: float
    lon: float


class ConsultaResponse(BaseModel):
    nombres: str
    apellido_paterno: Optional[str]
    apellido_materno: Optional[str]
    es_miembro_mesa: bool
    lugar_votacion: Lugar


def _carga_datos(path: str = None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "data", "people.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


DATA = _carga_datos()


def _validar_dni(dni: str) -> bool:
    return dni.isdigit() and len(dni) == 8


def _calcular_digito(dni: str) -> str:
    # Suma de dígitos mod 10 (mock)
    return str(sum(int(d) for d in dni) % 10)


@app.post("/api/consulta", response_model=ConsultaResponse)
def consulta(req: ConsultaRequest):
    if not _validar_dni(req.dni):
        raise HTTPException(status_code=400, detail="DNI inválido. Debe contener 8 dígitos.")

    if not req.digito_verificador.isdigit() or len(req.digito_verificador) != 1:
        raise HTTPException(status_code=400, detail="Dígito verificador inválido.")

    persona = next((p for p in DATA if p.get("dni") == req.dni and p.get("fecha_emision") == req.fecha_emision.isoformat()), None)
    if not persona:
        raise HTTPException(status_code=404, detail="No se encontró la persona con los datos proporcionados.")

    # Preferir el dígito almacenado en los datos; si no existe, calcular como fallback
    registrado = persona.get("digito_verificador")
    esperado = registrado if registrado is not None else _calcular_digito(req.dni)
    if req.digito_verificador != esperado:
        raise HTTPException(status_code=400, detail="Dígito verificador no coincide con el registro.")

    lugar = persona.get("lugar_votacion", {})

    return ConsultaResponse(
        nombres=persona.get("nombres"),
        apellido_paterno=persona.get("apellido_paterno"),
        apellido_materno=persona.get("apellido_materno"),
        es_miembro_mesa=persona.get("es_miembro_mesa", False),
        lugar_votacion=Lugar(
            nombre=lugar.get("nombre", "-"),
            lat=lugar.get("lat", 0.0),
            lon=lugar.get("lon", 0.0),
        ),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
