from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routers import auth, availability, appointments, health

app = FastAPI(title=settings.PROJECT_NAME)

# CORS
origins = settings.allowed_origins_list
allow_credentials = origins != ["*"]  # no credentials when wildcard
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas solo si así se configuró (útil para primer deploy)
if settings.AUTO_CREATE_TABLES:
    Base.metadata.create_all(bind=engine)

# Routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(availability.router)
app.include_router(appointments.router)
