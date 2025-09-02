# 🛰️ Sistema de Monitoramento de Satélites

## 📖 Sobre o Projeto

Este é um **sistema web completo** para monitoramento de satélites em tempo real. Imagine um painel de controle espacial moderno, como aqueles que você vê em filmes de ficção científica, mas real e funcional!

O sistema permite acompanhar o status e dados de telemetria de três satélites importantes:
- **Hubble Space Telescope** - O famoso telescópio espacial
- **ISS (International Space Station)** - A Estação Espacial Internacional  
- **NOAA-19** - Satélite meteorológico

## 🎯 O que o Sistema Faz

### 📊 **Monitoramento em Tempo Real**
- Mostra se os satélites estão ativos ou inativos
- Exibe dados de temperatura e nível de bateria
- Acompanha a posição orbital (latitude, longitude, altitude)
- Atualiza automaticamente a cada 5 segundos

### 🎨 **Interface Moderna**
- Design estilo "painel de controle espacial"
- Cores escuras com detalhes em azul ciano
- Animações e efeitos visuais
- Gráficos interativos para temperatura e bateria
- Totalmente responsivo (funciona no celular e computador)

### 🔧 **Arquitetura Robusta**
- **Dois serviços independentes**: Se um falhar, o outro continua funcionando
- **Dados simulados realistas**: Posições orbitais e telemetria baseadas em dados reais
- **Pronto para integração**: Pode facilmente conectar com APIs reais de satélites

## 🏗️ Estrutura do Projeto

```
satellite_monitoring/
├── 📁 service1_status/          # Serviço de Status dos Satélites
│   └── main.py                  # Gerencia informações básicas dos satélites
├── 📁 service2_telemetry/       # Serviço de Telemetria
│   └── main.py                  # Coleta dados em tempo real
├── 📁 frontend/                 # Interface do Usuário
│   ├── index.html              # Página principal
│   ├── styles.css              # Estilos visuais
│   └── script.js               # Funcionalidades
├── requirements.txt            # Dependências Python
├── start_services.py           # Script para iniciar tudo
└── README.md                   # Este arquivo
```

## 🚀 Como Usar (Simplificado)

1) Pré‑requisitos
- Python 3.10+
- PostgreSQL (para Status) e MySQL (para Telemetria)

2) Ambiente e dependências
```powershell
cd C:\Users\heito\Downloads\Microservices-P1-main\Microservices-P1-main
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi "uvicorn[standard]" sqlalchemy pydantic psycopg2-binary pymysql
```

3) Bancos (uma única vez)
- Crie os bancos vazios (tabelas são criadas automaticamente no primeiro start):
  - PostgreSQL: `satellite_status`
  - MySQL: `satellite_telemetry`

4) (Opcional) Variáveis de ambiente do PostgreSQL
```powershell
$env:PG_USER="postgres"; $env:PG_PASSWORD="SUA_SENHA"; $env:PG_HOST="localhost"; $env:PG_PORT="5432"; $env:PG_DB="satellite_status"
```

5) Rodar tudo de uma vez
```powershell
python .\satellite_monitoring\start_services.py
```
Endereços:
- Status:     http://localhost:8001/health
- Telemetria: http://localhost:8002/health
- Frontend:   http://localhost:8080

Pare tudo com Ctrl+C.

Observações
- Se mudar a porta do frontend, ajuste CORS nos dois serviços.
- Se uma porta estiver ocupada, feche o processo ou edite o `start_services.py`.
- No frontend, a atualização em tempo real ocorre a cada 5s (mude `UPDATE_INTERVAL` em `frontend/script.js`).

## ▶️ Executar tudo em um único terminal (simplificado)

1) Ative o venv e instale dependências (se ainda não fez)
```powershell
cd C:\Users\SEU_USUARIO\Downloads\Microservices-P1-main\Microservices-P1-main
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi "uvicorn[standard]" sqlalchemy pydantic psycopg2-binary pymysql
```

2) (Opcional) Exporte variáveis do PostgreSQL para o serviço de Status (8001)
```powershell
$env:PG_USER="postgres"
$env:PG_PASSWORD="SUA_SENHA"
$env:PG_HOST="localhost"
$env:PG_PORT="5432"
$env:PG_DB="satellite_status"
```

3) Rode o script de inicialização
```powershell
python .\satellite_monitoring\start_services.py
```

Isso inicia:
- Status:     http://localhost:8001/health
- Telemetria: http://localhost:8002/health
- Frontend:   http://localhost:8080

Pare tudo com Ctrl+C no mesmo terminal.

Observações
- As tabelas são criadas automaticamente na primeira execução de cada serviço.
- Se a porta estiver ocupada, feche o processo ou ajuste as portas no script.
- CORS já permite `http://localhost:8080` (se mudar a porta do frontend, ajuste nos serviços).

## 👥 Integrantes do Projeto

- Heitor Santos Cortes
- Paulo Henrique Amaral

---

**Desenvolvido com 🚀 para monitoramento espacial em tempo real**
