# Deploy a Producción (Render)

## 1) Variables de entorno
- `DATABASE_URL` → `postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME`
- `SECRET_KEY` → cadena aleatoria larga
- `ALLOWED_ORIGINS` → ej: `https://tu-frontend.com,https://psico-demo.onrender.com`
- `CORS_ALLOW_ALL` → `false`
- `ENV` → `prod`
- `AUTO_CREATE_TABLES` → `true` (solo primer despliegue)
- (Opcional) `SENDGRID_API_KEY`

## 2) Build/Start
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 3) DB
Postgres con URL `postgresql+psycopg://...`
