# 📌 Projeto: Aplicação Cliente-Servidor com Microsserviços

## 🎯 Objetivo
Este projeto tem como objetivo desenvolver uma aplicação cliente-servidor utilizando **arquitetura de microsserviços** para o backend, com foco principal no **projeto e implementação do banco de dados**.

## 🏗️ Estrutura da Aplicação
A aplicação é dividida em três camadas principais:

1. **Frontend (Cliente)**
   - Desenvolvido em **HTML, CSS e JavaScript**.
   - Responsável pela interface com o usuário.
   - Consome as APIs REST expostas pelo backend.

2. **Backend (Microsserviços)**
   - Implementado em **Python** (FastAPI/Flask).
   - Cada serviço é independente e focado em uma funcionalidade específica.
   - Comunicação via **APIs REST**.
   - Um **API Gateway** centraliza as requisições do cliente.

3. **Banco de Dados**
   - Utiliza **MySQL**, gerenciado com **DBeaver**.
   - Cada microsserviço possui seu próprio esquema de banco de dados.
   - Segue boas práticas de normalização e modelagem.

## ⚙️ Ferramentas Utilizadas
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (FastAPI/Flask)  
- **Banco de Dados:** MySQL (com DBeaver para administração)  
- **Controle de Versão:** Git/GitHub  

## 🚀 Como Executar
1. **Clonar o repositório**
   ```bash
   git clone https://github.com/seu-usuario/Microservices-P1.git
   ```

2. **Configurar o Backend**
   - Instalar dependências:
     ```bash
     pip install -r requirements.txt
     ```
   - Rodar o microsserviço:
     ```bash
     uvicorn main:app --reload
     ```

3. **Configurar o Banco de Dados**
   - Criar o banco no MySQL.
   - Executar os scripts SQL disponíveis em `/db`.

4. **Rodar o Frontend**
   - Abrir o arquivo `index.html` no navegador.

## 📊 Exemplos de Funcionalidades
- Cadastro e autenticação de usuários.  
- Consulta de dados por meio das APIs.  
- Persistência de informações em banco de dados.  

## 👥 Equipe
- Nome do Integrante 1  
- Nome do Integrante 2  
- Nome do Integrante 3  
- Nome do Integrante 4  

---
📅 **Entrega:** 09/09  
