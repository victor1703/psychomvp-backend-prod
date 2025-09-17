# PsicoMVP — Backend FastAPI (Producción)

Listo para deploy en Render/Railway.
- Postgres con psycopg3
- CORS configurable
- `AUTO_CREATE_TABLES` para primer deploy

## Local rápido
```bash
cp .env.local.example .env
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run.sh
```
Abrí: http://localhost:8000/docs

## Producción
Ver `README_DEPLOY.md` y `.env.prod.example`.
