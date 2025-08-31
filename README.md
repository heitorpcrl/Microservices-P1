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

## 🚀 Como Usar

### 1. **Iniciar o Sistema**
```bash
python start_services.py
```

### 2. **Acessar a Interface**
- Abra o arquivo `frontend/index.html` no navegador
- Ou acesse: http://localhost:8080 (se usar servidor local)

### 3. **Navegar pelo Sistema**
- **Página Inicial**: Lista todos os satélites com status
- **Clicar em um Satélite**: Abre a página de monitoramento detalhado
- **Dados em Tempo Real**: Atualização automática a cada 5 segundos

## 📱 Funcionalidades Principais

### **Página de Lista de Satélites**
- Visão geral de todos os satélites
- Status ativo/inativo com indicadores visuais
- Informações básicas (órbita, tempo operacional)
- Design em cards interativos

### **Página de Monitoramento**
- **Seção de Status**: Dados básicos do satélite
- **Seção de Telemetria**: 
  - Gráficos de temperatura e bateria
  - Posição atual em coordenadas
  - Indicador de dados ao vivo
  - Última atualização

## 🎨 Características Visuais

- **Tema Espacial**: Cores escuras com detalhes em azul ciano
- **Animações**: Efeitos de brilho, partículas flutuantes, transições suaves
- **Responsivo**: Funciona perfeitamente em desktop, tablet e celular
- **Feedback Visual**: Indicadores de status, loading, hover effects

## 🔮 Próximos Passos

O sistema está preparado para:
- Integração com APIs reais de satélites
- Adição de mais satélites
- Mapa interativo da posição orbital
- Alertas e notificações
- Histórico de dados mais extenso

## 💡 Por que Este Projeto?

Este projeto demonstra como criar um sistema moderno de monitoramento usando:
- **Arquitetura de microsserviços** (serviços independentes)
- **Interface web moderna** com HTML, CSS e JavaScript
- **Dados em tempo real** com atualizações automáticas
- **Design responsivo** para todos os dispositivos

É perfeito para aprender sobre desenvolvimento web, APIs, e como criar interfaces modernas e funcionais!

---

**Desenvolvido com 🚀 para monitoramento espacial em tempo real**
