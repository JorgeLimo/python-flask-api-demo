# ============================================================================
# config.py — Configuración de la aplicación y conexión a la base de datos
# ============================================================================
import os
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env
load_dotenv()


def obtener_database_uri():
    """
    Lee la cadena de conexión desde la variable de entorno DATABASE_URL
    (la que te da Neon) y la adapta para que SQLAlchemy la entienda.
    """
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "Falta la variable de entorno DATABASE_URL.\n"
            "Crea un archivo .env (puedes copiar .env.example) y pega ahí "
            "la cadena de conexión que te da Neon."
        )

    # SQLAlchemy necesita el driver "psycopg" explícito en la URL
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    return database_url


class Config:
    """Agrupa toda la configuración de Flask en un solo lugar."""
    SQLALCHEMY_DATABASE_URI = obtener_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False