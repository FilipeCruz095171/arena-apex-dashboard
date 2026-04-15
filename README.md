# 🛡️ Arena Apex Analytics

**Arena Apex Analytics** é um dashboard interativo construído em **Python & Streamlit** voltado para o cenário eSports competitivo de Apex Legends (Custom Lobbies & Campeonatos da comunidade Arena Apex). A plataforma consome dados diretos da **Apex Legends Status (ALS) API** para fornecer análises consistentes de performance de jogadores.

---

## 🔥 Principais Funcionalidades

- **Métrica APS (Apex Performance Score):** Um poderoso sistema de ranking que pondera Kills, Assists e Dano em conjunto com um "Multiplicador de Consistência" logarítmico, desencorajando jogadores de baixa amostragem de vitórias isoladas.
- **Comparação 1v1 Avançada:** Sistema de comparação direta gráfica entre dois jogadores, com radar e evolução cronológica lado-a-lado usando a identidade visual da guilda.
- **Consolidação por ID único:** Controle independente das mudanças de nick dos usuários. O progresso histórico é vinculado à conta, proporcionando rastreio completo não importa se o jogador mudou de nome dezenas de vezes.
- **Layout Premium & Brand Identity:** UI altamente estilizada (Dark Ruby) focada para a estética agresiva de jogos eletrônicos.
- **Cálculo Oficial:** Exibição da tabela crua baseada no `Kill Cap` estipulado pelas regras competitivas da etapa.

## 🛠️ Tecnologias Utilizadas

- `Streamlit` (Web App Framework & UI)
- `Pandas` (Processamento Rápido de DataFrames em Cache)
- `Plotly` (Gráficos interativos Dinâmicos de DataViz)
- `Requests & Dotenv` (Integrações com API Externa RESTful)

---

## 🚀 Como testar localmente na sua máquina

### 1. Requisitos Prévios
- Python 3.10+
- Git

### 2. Instalação
Faça o clone do repositório contendo a base de arquivos:
```bash
git clone https://github.com/SEU_GITHUB/arena-apex-dashboard.git
cd arena-apex-dashboard
```

Instale as dependências requisitadas para o motor funcionar:
```bash
pip install -r requirements.txt
```

### 3. Configurando as Variáveis Secretas
Para consumir os dados da ALS API, crie um arquivo chamado `.env` solto na pasta principal com o seu Token e Cookie de sessão capturados diretamente pelo painel administrativo:
```toml
# Arquivo: .env
ALS_API_TOKEN="seu_token_api_aqui"
ALS_SESSION_COOKIE="seu_cookie_da_api_aqui"
```

### 4. Iniciando a aplicação
Rode o comando de execução nativo do Streamlit:
```bash
streamlit run main.py
```
A plataforma irá abrir instantaneamente em http://localhost:8501 no o seu navegador.

---
*Este projeto foi inteiramente desenhado para fomentar o aspecto analítico/coach do competitivo de Apex Legends para membros e players ativos da divisão Arena Apex.*
