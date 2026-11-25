# SHA-1 NL v1.0

Aplicación académica de una variante experimental basada en SHA-1.

## Requisitos
- Python 3.10 o superior
- pip

## Instalación
```bash
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar la aplicación
```bash
python app.py
```
Abrir en el navegador: http://127.0.0.1:5000

## Ejecutar pruebas
Desde la carpeta raíz:
```bash
python -m unittest discover -s tests -v
```

## Archivos principales
- `algorithm/operations.py`: operaciones booleanas y funciones NL.
- `algorithm/expansion.py`: expansión de 16 a 80 palabras.
- `algorithm/sha1_nl.py`: padding, compresión y digest.
- `tests/`: pruebas automatizadas.
- `documentation/`: justificación matemática.

## Aviso
SHA-1 NL es experimental y educativo. No utilizar para seguridad real.
