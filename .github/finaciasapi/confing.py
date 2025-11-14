import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLITE_PATH = os.path.join(BASE_DIR, "app.db")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mudar_esta_chave_para_producao")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "mudar_esta_chave_jwt")
