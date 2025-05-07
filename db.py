'''Este es el archivo con la conexión a la DB.'''
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from models import Usuario, Tarea

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tareadb.db")

CLEVER_DB = None
if all([os.getenv(f"CLEVER_{key}") for key in ["USER", "PASSWORD", "HOST", "PORT", "DATABASE"]]):
    CLEVER_DB = (
        f"postgresql://{os.getenv('CLEVER_USER')}:" 
        f"{os.getenv('CLEVER_PASSWORD')}@" 
        f"{os.getenv('CLEVER_HOST')}:" 
        f"{os.getenv('CLEVER_PORT')}/" 
        f"{os.getenv('CLEVER_DATABASE')}"
    )

FINAL_DB_URL = CLEVER_DB if CLEVER_DB else DATABASE_URL

engine = create_engine(FINAL_DB_URL, echo=os.getenv("DEBUG", "False").lower() == "true")


def crear_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session