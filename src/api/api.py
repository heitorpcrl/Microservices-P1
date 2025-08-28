from fastapi import APIRouter
from src.api.endpoints import users

# Router principal da API
api_router = APIRouter()

# Incluir rotas de usuários
api_router.include_router(users.router)

# Aqui você pode incluir outros roteadores conforme necessário
# api_router.include_router(auth.router)
# api_router.include_router(products.router)
# etc.
