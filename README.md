
# Instructivo: ONPE Mock API (rápido y práctico)
#dddd
Este proyecto es una API de demostración que devuelve el lugar de votación y si la persona es miembro de mesa, a partir de:
- `dni` (8 dígitos)
- `fecha_emision` (YYYY-MM-DD)
- `digito_verificador` (1 dígito)

Archivos relevantes:
- `main.py` — servidor FastAPI con el endpoint POST `/api/consulta`.
- `data/people.json` — datos de ejemplo (registros con `dni`, `fecha_emision`, `nombres`, `es_miembro_mesa`, `lugar_votacion`).

Requisitos
- Python 3.10+ (o la versión que tengas instalada). Se recomienda usar un virtualenv.

Pasos (PowerShell en Windows)

1) Crear y activar entorno virtual (opcional pero recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3) Ejecutar la API (modo desarrollo):

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
# o alternativamente
python main.py
```

4) Abrir Swagger UI para probar de forma interactiva (local):

  http://127.0.0.1:8000/docs

Si ya desplegaste en Azure, tu URL pública es:

  https://onpe-d7avgtemcnfqedaj.canadacentral-01.azurewebsites.net

Y la documentación interactiva en producción estará en:

  https://onpe-d7avgtemcnfqedaj.canadacentral-01.azurewebsites.net/docs

5) Ejemplo de petición (PowerShell - Invoke-RestMethod) — local y en Azure:

Local:
```powershell
$body = @{ dni = '12345678'; fecha_emision = '2015-03-10'; digito_verificador = '6' } | ConvertTo-Json
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/consulta' -Method Post -Body $body -ContentType 'application/json'
```

En Azure (reemplaza con tu URL si es otra):
```powershell
$body = @{ dni = '12345678'; fecha_emision = '2015-03-10'; digito_verificador = '6' } | ConvertTo-Json
Invoke-RestMethod -Uri 'https://onpe-d7avgtemcnfqedaj.canadacentral-01.azurewebsites.net/api/consulta' -Method Post -Body $body -ContentType 'application/json'
```

Respuesta esperada (Formato JSON):

{
  "nombres": "Juan Carlos",
  "apellido_paterno": "Perez",
  "apellido_materno": "Gonzalez",
  "es_miembro_mesa": true,
  "lugar_votacion": { "nombre": "IE San Miguel", "lat": -12.0464, "lon": -77.0428 }
}

Notas importantes
- Este proyecto es un mock: el dígito verificador se valida con una regla de ejemplo (suma de los dígitos mod 10). No es necesariamente el algoritmo real del RENIEC/ONPE.
- Para producción deberías reemplazar `data/people.json` por una base de datos y asegurar la autenticidad de los datos.

Tests
- Ejecutar los tests unitarios creados con pytest:

```powershell
python -m pytest -q
```

Dónde modificar datos de ejemplo
- `data/people.json` contiene varios registros de ejemplo. Puedes editarlo para añadir/quitar entradas.

Si quieres que automatice la migración a una base de datos SQLite, añada autenticación o implemente el algoritmo oficial del dígito verificador, dímelo y lo preparo.
