import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Configurações da API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Configurações de Segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "chave_secreta_padrao")
    
    # Configurações do Banco
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://usuario:senha@localhost:5432/nome_banco")

# Instância global das configurações
settings = Settings()
