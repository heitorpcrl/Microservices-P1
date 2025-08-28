#!/usr/bin/env python3
"""
Script para configuração inicial do banco de dados
"""
import os
import sys
from dotenv import load_dotenv

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.config.database import engine
from src.models.user import Base

def setup_database():
    """Criar todas as tabelas no banco de dados"""
    try:
        print("Criando tabelas no banco de dados...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False
    
    return True

def main():
    """Função principal"""
    load_dotenv()
    
    print("🚀 Configurando banco de dados...")
    
    if setup_database():
        print("🎉 Configuração concluída com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Configure suas variáveis de ambiente no arquivo .env")
        print("2. Execute: python -m uvicorn src.main:app --reload")
        print("3. Acesse: http://localhost:8000/docs")
    else:
        print("💥 Falha na configuração do banco de dados")
        sys.exit(1)

if __name__ == "__main__":
    main()
