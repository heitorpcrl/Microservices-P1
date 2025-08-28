# API FastAPI - Estrutura Básica

Uma API REST básica construída com FastAPI, SQLAlchemy e PostgreSQL, organizada com uma estrutura modular e escalável.

## 🏗️ Estrutura do Projeto

```
Microservices-P1/
├── src/                    # Código fonte da aplicação
│   ├── api/               # Camada de API e rotas
│   │   ├── endpoints/     # Endpoints específicos
│   │   └── api.py         # Roteador principal
│   ├── config/            # Configurações
│   │   ├── database.py    # Configuração do banco
│   │   └── settings.py    # Configurações gerais
│   ├── crud/              # Operações CRUD
│   │   └── user.py        # Operações de usuário
│   ├── models/            # Modelos do banco de dados
│   │   └── user.py        # Modelo de usuário
│   ├── schemas/           # Schemas Pydantic
│   │   └── user.py        # Schemas de usuário
│   └── main.py            # Aplicação principal
├── alembic/               # Migrações do banco
├── tests/                 # Testes automatizados
├── scripts/               # Scripts utilitários
├── requirements.txt       # Dependências Python
├── alembic.ini           # Configuração do Alembic
└── env_example.txt       # Exemplo de variáveis de ambiente
```

## 🚀 Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para APIs
- **SQLAlchemy**: ORM para Python
- **PostgreSQL**: Banco de dados relacional
- **Alembic**: Sistema de migrações
- **Pydantic**: Validação de dados
- **Uvicorn**: Servidor ASGI

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL
- DBeaver (ou outro cliente SQL)

## 🛠️ Instalação

1. **Clone o repositório e navegue até o diretório:**
   ```bash
   cd Microservices-P1
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   - Copie `env_example.txt` para `.env`
   - Edite o arquivo `.env` com suas configurações de banco

5. **Configure o banco de dados:**
   ```bash
   python scripts/setup_database.py
   ```

## 🚀 Executando a Aplicação

### Desenvolvimento
```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Produção
```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## 📚 Documentação da API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗄️ Banco de Dados

### Configuração
- Edite o arquivo `.env` com suas credenciais do PostgreSQL
- Use DBeaver para conectar e gerenciar o banco

### Migrações
```bash
# Criar nova migração
alembic revision --autogenerate -m "Descrição da migração"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1
```

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=src

# Executar testes específicos
pytest tests/test_users.py
```

## 📁 Endpoints Disponíveis

### Usuários
- `POST /api/v1/users/` - Criar usuário
- `GET /api/v1/users/` - Listar usuários
- `GET /api/v1/users/{id}` - Obter usuário específico
- `PUT /api/v1/users/{id}` - Atualizar usuário
- `DELETE /api/v1/users/{id}` - Deletar usuário

### Sistema
- `GET /` - Endpoint raiz
- `GET /health` - Verificação de saúde

## 🔧 Configurações

### Variáveis de Ambiente
- `DATABASE_URL`: URL de conexão com o banco
- `API_HOST`: Host da API (padrão: 0.0.0.0)
- `API_PORT`: Porta da API (padrão: 8000)
- `DEBUG`: Modo debug (padrão: True)
- `SECRET_KEY`: Chave secreta para segurança

## 📝 Exemplo de Uso

### Criar um usuário
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "usuario_teste",
       "email": "teste@exemplo.com",
       "full_name": "Usuário de Teste",
       "password": "senha123"
     }'
```

### Listar usuários
```bash
curl "http://localhost:8000/api/v1/users/"
```

## 🚧 Próximos Passos

- [ ] Implementar autenticação JWT
- [ ] Adicionar validação de senhas
- [ ] Implementar logs estruturados
- [ ] Adicionar cache Redis
- [ ] Implementar rate limiting
- [ ] Adicionar documentação mais detalhada

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🆘 Suporte

Se você encontrar algum problema ou tiver dúvidas, abra uma issue no repositório.
