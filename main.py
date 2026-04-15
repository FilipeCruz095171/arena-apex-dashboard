import streamlit as st
import pandas as pd
import requests
import os
import time
from dotenv import load_dotenv
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# 1. Configuração Inicial da Página
st.set_page_config(page_title="Arena Apex Analytics", page_icon="🛡️", layout="wide")

def injetar_css_arena_apex():
    st.markdown("""
        <style>
            /* Reset e Fonte global */
            @import url('https://fonts.googleapis.com/css2?family=Teko:wght@500;700&family=Montserrat:wght@400;600;800&display=swap');
            
            html, body, [class*="css"] {
                font-family: 'Montserrat', sans-serif;
            }
            
            /* Títulos agressivos */
            h1, h2, h3 {
                font-family: 'Teko', sans-serif !important;
                letter-spacing: 1px;
                text-transform: uppercase;
                color: #FFFFFF !important;
            }
            
            /* Fundo da tela inteira (Gradient escuro avermelhado) */
            .stApp {
                background: radial-gradient(circle at 50% 0%, #301318 0%, #170d14 60%, #0d0a0f 100%) !important;
            }
            
            /* Header do Streamlit transparente */
            header { background-color: transparent !important; }
            
            /* Ocultar link âncora nos títulos */
            .st-emotion-cache-10trblm { display: none !important; }
            
            /* Título principal do Dashboard */
            .title-brand {
                font-family: 'Teko', sans-serif;
                font-size: 56px;
                background: -webkit-linear-gradient(45deg, #FF2B35, #A91012);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin-top: -30px;
                margin-bottom: 30px;
                text-transform: uppercase;
                letter-spacing: 3px;
                text-shadow: 0px 4px 20px rgba(227,27,35,0.2);
            }
            
            /* Melhoria visual nas abas (Tabs) */
            .stTabs [data-baseweb="tab-list"] {
                gap: 15px;
                border-bottom: 2px solid #301318;
            }
            .stTabs [data-baseweb="tab"] {
                background-color: rgba(20, 10, 15, 0.6);
                border-radius: 6px 6px 0px 0px;
                padding: 10px 20px;
                color: #A0A0A0;
                font-family: 'Teko', sans-serif;
                font-size: 22px;
                border: 1px solid transparent;
                border-bottom: none;
                transition: all 0.2s ease-in-out;
            }
            .stTabs [data-baseweb="tab"]:hover {
                color: #FFF;
                background-color: rgba(227, 27, 35, 0.1);
            }
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                color: #FFFFFF !important;
                background-color: #E31B23;
                border-color: #E31B23;
                box-shadow: 0 -4px 15px rgba(227, 27, 35, 0.4);
            }
            
            /* Botão primário (Gerar Análise) */
            .stButton > button {
                width: 100%;
                background: linear-gradient(90deg, #A91012 0%, #E31B23 100%);
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 800;
                font-family: 'Montserrat', sans-serif;
                text-transform: uppercase;
                padding: 15px !important;
                box-shadow: 0 4px 15px rgba(227, 27, 35, 0.3);
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                background: linear-gradient(90deg, #E31B23 0%, #FF2B35 100%);
                box-shadow: 0 4px 25px rgba(227, 27, 35, 0.6);
                transform: translateY(-2px);
                color: white;
            }
            
            /* Cards de Métricas */
            div[data-testid="stMetric"] {
                background-color: rgba(20, 10, 15, 0.7);
                border-left: 4px solid #E31B23;
                padding: 15px;
                border-radius: 0px 5px 5px 0px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            }
            div[data-testid="stMetricValue"] {
                color: #FFFFFF;
                font-family: 'Teko', sans-serif;
                font-size: 38px !important;
            }
            div[data-testid="stMetricDelta"] {
                color: #aaaaaa;
            }
            
            /* Alertas e Expander */
            div.stAlert {
                background-color: rgba(30, 15, 20, 0.8) !important;
                color: #FFFFFF !important;
                border-radius: 6px;
                border: 1px solid #4A171C !important;
                border-left: 5px solid #E31B23 !important;
            }
            div.stExpander {
                background-color: rgba(20, 10, 15, 0.5) !important;
                border: 1px solid #4A171C !important;
                border-radius: 6px;
            }
            
            /* Inputs e Selectbox */
            .stSelectbox > div > div {
                background-color: rgba(20, 10, 15, 0.8) !important;
                color: white !important;
                border: 1px solid #4A171C !important;
            }
            
            /* Melhoria no Menu Lateral (Sidebar) */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #170d14 0%, #2b0b11 50%, #170d14 100%) !important;
                border-right: 2px solid #4A171C !important;
            }
            [data-testid="stSidebar"] * {
                color: #F5F5F5 !important;
            }
            [data-testid="stSidebar"] .derby-text {
                color: #E31B23 !important;
                font-weight: 800 !important;
            }
            [data-testid="stSidebar"] .stButton > button {
                background: rgba(20, 10, 15, 0.4);
                border: 1px solid #E31B23;
                box-shadow: none;
            }
            [data-testid="stSidebar"] .stButton > button:hover {
                background: #E31B23;
            }
            
        </style>
    """, unsafe_allow_html=True)

injetar_css_arena_apex()

# --- CARREGAMENTO DO LOGO ---
import base64
import os

def render_header():
    # Streamlit Cloud é Linux (Sensível a letras maiúsculas/minúsculas)
    logo_path = "LOGO.png" if os.path.exists("LOGO.png") else "logo.png"
    
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        logo_html = f'''
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: -50px; margin-bottom: 40px;">
            <img src="data:image/png;base64,{encoded_string}" style="height: 180px; filter: drop-shadow(0px 10px 25px rgba(227,27,35,0.8)); margin-bottom: 15px; transform: scale(1.05);">
            <div class='title-brand' style="margin: 0; padding: 0;">ARENA APEX ANALYTICS</div>
        </div>
        '''
        st.markdown(logo_html, unsafe_allow_html=True)
    else:
        st.markdown("<h1 class='title-brand'>🛡️ ARENA APEX ANALYTICS</h1>", unsafe_allow_html=True)

render_header()

# ---------------------------------------------------------
# NOVIDADE: CRIANDO A "MEMÓRIA" DO DASHBOARD
# ---------------------------------------------------------
if "dados_extraidos" not in st.session_state:
    st.session_state.dados_extraidos = False
if "df_players" not in st.session_state:
    st.session_state.df_players = pd.DataFrame()
if "etapas_processadas" not in st.session_state:
    st.session_state.etapas_processadas = []
if "dicionario_etapas" not in st.session_state:
    st.session_state.dicionario_etapas = {}

# 2. Carregar o Token do .env
load_dotenv()
TOKEN = os.getenv("ALS_API_TOKEN")
SESSION_COOKIE = os.getenv("ALS_SESSION_COOKIE", "")

if not TOKEN:
    st.error("⚠️ Token da API não encontrado. Verifique seu arquivo .env.")
    st.stop()

HEADERS = {"Authorization": TOKEN}
# O cookie de sessão é necessário além do token para a API funcionar
COOKIES = {"apexlegendsstatus_ssid": SESSION_COOKIE} if SESSION_COOKIE else {}

if not SESSION_COOKIE:
    st.warning(
        "🔑 **Cookie de sessão não configurado.** A API requer um cookie de login além do token.\n\n"
        "**Como configurar:**\n"
        "1. Abra o site logado como `arenaapex` no browser\n"
        "2. Pressione F12 → aba **Application** → **Cookies** → `apexlegendsstatus.com`\n"
        "3. Copie o valor do cookie **`apexlegendsstatus_ssid`**\n"
        "4. Adicione no arquivo `.env`: `ALS_SESSION_COOKIE=valor_copiado`\n"
        "5. Reinicie o Streamlit"
    )


# 3. Funções de Extração (ESSENCIAIS)
@st.cache_data(ttl=300)
def get_tournaments():
    url = "https://apexlegendsstatus.com/tournament/saturne/api/tournaments"
    delays = [0, 2, 5]  # Backoff: tenta imediatamente, depois 2s, depois 5s
    for delay in delays:
        try:
            if delay:
                time.sleep(delay)
            response = requests.get(url, headers=HEADERS, cookies=COOKIES, timeout=15)
            if response.status_code == 200:
                return response.json()
        except Exception:
            continue
    return []  # Retorna lista vazia sem travar o app


@st.cache_data(ttl=300)
def get_scores(tournament_id):
    url = f"https://apexlegendsstatus.com/tournament/saturne/api/scores?tournamentId={tournament_id}"
    for _ in range(3):
        try:
            response = requests.get(url, headers=HEADERS, cookies=COOKIES, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and "teamData" in data and len(data["teamData"]) > 0:
                    return data
            time.sleep(1)
        except:
            continue
    return None

@st.cache_data(ttl=300)
def get_game_scores(tournament_id, game_id: str):
    """Busca dados de uma partida individual pelo gameId.
    Endpoint confirmado: /scores?tournamentId=X&gameId=Y
    NOTA: retorna dados CUMULATIVOS, nao por partida."""
    url = (
        f"https://apexlegendsstatus.com/tournament/saturne/api/scores"
        f"?tournamentId={tournament_id}&gameId={game_id}"
    )
    try:
        r = requests.get(url, headers=HEADERS, cookies=COOKIES, timeout=10)
        if r.status_code == 200:
            d = r.json()
            if d and "teamData" in d:
                return d
    except Exception:
        pass
    return None

@st.cache_data(ttl=300)
def get_html_scores(tournament_id: int) -> dict:
    """Extrai pontuacoes CORRETAS (com Kill Cap ja aplicado) da pagina HTML do site.
    Retorna: {team_name: {"score": int, "kills_raw": int, "rank": int}}
    Fonte primaria para a Aba 3."""
    from bs4 import BeautifulSoup
    url = f"https://apexlegendsstatus.com/tournament/results/{tournament_id}/Overview"
    headers_html = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "pt-BR,pt;q=0.9",
    }
    try:
        r = requests.get(url, headers=headers_html, cookies=COOKIES, timeout=15)
        if r.status_code != 200:
            return {}
        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.find_all(class_="score-table_row")
        result = {}
        for row in rows:
            name_el  = row.find(class_="team-name")
            score_el = row.find(class_="team-score")
            kills_el = row.find(class_="team-kills")
            rank_el  = row.find(class_="rank-number")
            if name_el and score_el:
                name  = name_el.get_text(strip=True)
                score = int(score_el.get_text(strip=True))
                kills = int(kills_el.get_text(strip=True)) if kills_el else 0
                rank  = int(rank_el.get_text(strip=True)) if rank_el else 0
                result[name] = {"score": score, "kills_raw": kills, "rank": rank}
        return result
    except Exception:
        return {}

PLACEMENT_PTS = {
    1: 12, 2: 9, 3: 7, 4: 5, 5: 4, 6: 3,
    7: 2, 8: 2, 9: 2, 10: 2,
    11: 1, 12: 1, 13: 1, 14: 1, 15: 1,
}
KILL_CAP = 10

def calc_placement_pts(position: int) -> int:
    return PLACEMENT_PTS.get(int(position), 0)


# 4. Interface na Barra Lateral (Filtros)
st.sidebar.header("Filtros do Campeonato")
tournaments_data = get_tournaments()

# --- Verifica se a API respondeu ---
if not tournaments_data:
    st.error(
        "🚨 **API indisponível (erro 500)**\n\n"
        "O servidor apexlegendsstatus.com está retornando erro. "
        "Isso geralmente é temporário (rate limit ou instabilidade). "
        "Aguarde alguns minutos e clique em **Tentar Novamente**."
    )
    if st.button("🔄 Tentar Novamente"):
        st.cache_data.clear()
        st.rerun()
    st.stop()

if tournaments_data:
    for t in tournaments_data:
        latest_ts = 0
        if t.get('games'):
            timestamps = [g.get('uploadedAtUnixTimestamp', 0) for g in t['games'] if g.get('uploadedAtUnixTimestamp')]
            if timestamps:
                latest_ts = max(timestamps)
        if latest_ts > 1e11:
            latest_ts /= 1000
        t['date_obj'] = datetime.fromtimestamp(latest_ts) if latest_ts > 0 else datetime(2000, 1, 1)

    tournaments_data = sorted(tournaments_data, key=lambda x: x['date_obj'], reverse=True)

    st.sidebar.subheader("📅 Período das Etapas")
    valid_dates = [t['date_obj'].date() for t in tournaments_data if t['date_obj'].year > 2000]
    min_date = min(valid_dates) if valid_dates else datetime.today().date()
    max_date = max(valid_dates) if valid_dates else datetime.today().date()
    
    date_range = st.sidebar.date_input("Selecione o intervalo:", [min_date, max_date], min_value=min_date, max_value=max_date)
    filtro_nome = st.sidebar.text_input("🔍 Filtrar pelo nome da etapa:", "").lower()

    filtered_tournaments = []
    if len(date_range) == 2:
        start_date, end_date = date_range
    elif len(date_range) == 1:
        start_date, end_date = date_range[0], date_range[0]
    else:
        start_date, end_date = min_date, max_date

    for t in tournaments_data:
        t_date = t['date_obj'].date()
        if start_date <= t_date <= end_date and filtro_nome in t.get('name', '').lower() and t_date.year > 2000:
            filtered_tournaments.append(t)

    tournaments_dict = {f"{t['name']} ({t['date_obj'].strftime('%d/%m/%Y')})": t['id'] for t in filtered_tournaments}
    
    selecionar_todos = st.sidebar.checkbox("Selecionar todas as etapas filtradas")
    opcoes_padrao = list(tournaments_dict.keys()) if selecionar_todos else []
    
    selected_names = st.sidebar.multiselect("Etapas Selecionadas:", options=list(tournaments_dict.keys()), default=opcoes_padrao)

    # 5. O Botão Mágico (Agora salva na Memória)
    if st.sidebar.button("Gerar Análise") and selected_names:
        with st.spinner("Conectando ao banco de dados..."):
            all_players = []
            total_etapas = len(selected_names)
            barra_progresso = st.progress(0)
            texto_progresso = st.empty()
            
            # Salvando as etapas processadas na memória para a Aba 3 não dar erro
            st.session_state.etapas_processadas = selected_names
            st.session_state.dicionario_etapas = {name: tournaments_dict[name] for name in selected_names}
            
            for i, name in enumerate(selected_names):
                texto_progresso.text(f"📥 Baixando dados: {i+1} de {total_etapas} etapas...")
                t_id = tournaments_dict[name]
                scores = get_scores(t_id)
                t_name_clean = name.split(" (")[0]
                # Extrair a data do nome para ordenação cronológica
                try:
                    date_str = name.split("(")[-1].rstrip(")")
                    t_date_parsed = datetime.strptime(date_str, "%d/%m/%Y")
                except Exception:
                    t_date_parsed = datetime(2000, 1, 1)
                
                if scores and "teamData" in scores:
                    for team in scores["teamData"]:
                        if "playersData" in team:
                            for player in team["playersData"]:
                                all_players.append({
                                    "playerId": player.get("playerId"),
                                    "playerName": player.get("playerName"),
                                    "kills": player.get("kills", 0),
                                    "assists": player.get("assists", 0),
                                    "damageDealt": player.get("damageDealt", 0),
                                    "gamesPlayed": player.get("gamesPlayed", 0),
                                    "tournamentName": t_name_clean,
                                    "tournamentFullName": name,
                                    "tournamentDate": t_date_parsed,
                                })
                time.sleep(0.5) 
                barra_progresso.progress((i + 1) / total_etapas)
            
            texto_progresso.empty()
            barra_progresso.empty()
            
            # Guardando o DataFrame na memória da Sessão
            if all_players:
                st.session_state.df_players = pd.DataFrame(all_players)
                st.session_state.dados_extraidos = True
            else:
                st.session_state.dados_extraidos = False
                st.warning("Nenhum dado encontrado nas etapas selecionadas.")

    # Carregando a Imagem Assinatura do Autor
    derby_html = ""
    if os.path.exists("derby.jpg"):
        with open("derby.jpg", "rb") as f:
            derby_b64 = base64.b64encode(f.read()).decode()
        derby_html = f"<img src='data:image/jpeg;base64,{derby_b64}' style='width: 80px; height: 80px; object-fit: cover; border-radius: 50%; border: 2px solid #E31B23; box-shadow: 0px 4px 10px rgba(227, 27, 35, 0.4); margin-bottom: 10px;'><br>"

    st.sidebar.markdown(
        f"<div style='text-align: center; color: #666666; font-size: 13px; margin-top: 50px; border-top: 1px solid #4A171C; padding-top: 25px; font-family: Montserrat, sans-serif;'>"
        f"{derby_html}"
        "<b>Arena Apex Analytics v1.4.0</b><br>"
        "Crafted By <span class='derby-text'>Derby_Vermelho</span>"
        "</div>",
        unsafe_allow_html=True
    )

# ==========================================
# 6. EXIBIÇÃO DAS ABAS (FORA DO BOTÃO)
# ==========================================
if st.session_state.dados_extraidos:
    df = st.session_state.df_players

    aba1, aba2, aba3, aba4 = st.tabs([
        "📊 Ranking Consolidado",
        "📈 Analítico por Jogador",
        "🏁 Placar da Etapa (Lobby)",
        "🕵️‍♂️ CSI Arena"
    ])

    # --- CONTEÚDO DA ABA 1 ---
    with aba1:
        st.subheader("🏆 Ranking Consolidado: Rating de Performance")
        import math
        
        # Garante a ordenação cronológica para que o 'last' pegue o nick mais recente
        df_sorted = df.sort_values(by="tournamentDate", ascending=True)
        df_grouped = df_sorted.groupby("playerId").agg({
            "playerName": "last", "kills": "sum", "assists": "sum",
            "damageDealt": "sum", "gamesPlayed": "sum"
        }).reset_index()

        df_grouped = df_grouped[df_grouped["gamesPlayed"] > 0]
        max_games = df_grouped["gamesPlayed"].max() if not df_grouped.empty else 1
        
        # Captura todos os nicks únicos já vinculados a este ID e mapeia
        nicks_historicos = df_sorted.groupby("playerId")["playerName"].unique().apply(lambda x: ", ".join(x))
        df_grouped["Nicks_Anteriores"] = df_grouped["playerId"].map(nicks_historicos)
        
        # Cálculo das médias por partida
        df_grouped["KPR"] = df_grouped["kills"] / df_grouped["gamesPlayed"]
        df_grouped["APR"] = df_grouped["assists"] / df_grouped["gamesPlayed"]
        df_grouped["DPR"] = df_grouped["damageDealt"] / df_grouped["gamesPlayed"]
        
        # 1. Poder Base: Valorando pesos realistas do Apex Legends
        # Kill = 12pts, Assist = 8pts, 100 Dano = 1pt
        df_grouped["Poder_Base"] = (df_grouped["KPR"] * 12) + (df_grouped["APR"] * 8) + (df_grouped["DPR"] / 100)
        
        # 2. Fator de Consistência: Penaliza jogadores com poucas partidas
        df_grouped["Fator_Consistencia"] = df_grouped["gamesPlayed"].apply(
            lambda x: math.log2(x + 1) / math.log2(max_games + 1)
        )
        
        # 3. Rating Final (APS)
        df_grouped["APS"] = df_grouped["Poder_Base"] * df_grouped["Fator_Consistencia"]
        
        # Ordenação e limpeza
        df_grouped = df_grouped.sort_values(by="APS", ascending=False).reset_index(drop=True)
        df_grouped.index = df_grouped.index + 1 # Rank 1-based
        
        df_final = df_grouped[["playerId", "playerName", "kills", "assists", "damageDealt", "gamesPlayed", "KPR", "APR", "DPR", "APS"]]
        df_final.columns = ["ID da Conta", "Nick Atual", "Kills", "Assists", "Dano", "Partidas", "Kills/P", "Assists/P", "Dano/P", "Rating APS"]

        st.info(
            "📍 **O Segredo do APS (Apex Performance Score)**\n\n"
            "A métrica APS não se engana com sorte passageira. Ela trabalha em duas fases rigorosas para classificar o lobby:\n\n"
            "* **1️⃣ Fase 1 (Poder Bruto):** Primeiro calcula-se quão letal o jogador foi na média das vezes que pisou no mapa. Cada "
            "Kill vale 12pts, Assistência 8pts, e cada 100 de Dano vale 1pt.\n"
            "* **2️⃣ Fase 2 (A Guilhotina da Consistência):** Se o jogador participou de quase todas as partidas do mês, o sistema "
            "*preserva a maior parte* (85~100%) da nota de poder bruto dele. Mas, se ele jogou pouco (um \"turista\"), a matemática "
            "(através de uma curva Logarítmica) corta a pontuação cruelmente, caindo para menos da metade!\n\n"
            "**🎯 Resumo Prático:** Alguém que mata 6 jogadores em uma única partida e vai embora, não rouba o Top 1 de quem "
            "suou a camisa matando 3 jogadores por dezenas de partidas. O multiplicador barra os sortudos. A Média sustentada sempre vencerá a sorte isolada!", 
            icon="🧠"
        )

        tabela_estilizada = df_final.style.background_gradient(subset=["Rating APS"], cmap="YlOrRd").format({
            "Kills/P": "{:.2f}", "Assists/P": "{:.2f}", "Dano/P": "{:.0f}", "Rating APS": "{:.1f}"
        })
        st.dataframe(tabela_estilizada, use_container_width=True)

    # --- CONTEÚDO DA ABA 2 ---
    with aba2:
        st.subheader("📈 Painel Analítico do Jogador")
        # Consolidar jogadores pelo ID único para não perder histórico se mudarem de nick
        if "tournamentDate" in df.columns:
            df_recente = df.sort_values("tournamentDate")
        else:
            df_recente = df
        
        # Mapeamento do playerId para o playerName mais recente
        dict_jogadores = df_recente.groupby("playerId")["playerName"].last().to_dict()
        
        # Lista dos IDs ordenada alfabeticamente pelo nome para facilitar no selectbox
        lista_player_ids = sorted(dict_jogadores.keys(), key=lambda pid: str(dict_jogadores[pid]).lower())

        col_sel1, col_sel2, col_sel3 = st.columns([3, 1, 3])
        with col_sel1:
            jogador_selecionado_id = st.selectbox(
                "🎮 Jogador Principal:", 
                lista_player_ids, 
                format_func=lambda pid: dict_jogadores.get(pid, str(pid)),
                key="sel_player"
            )
            # Mantemos a variável com o nome para todos os subtítulos e gráficos!
            jogador_selecionado = dict_jogadores.get(jogador_selecionado_id, "")
            
        with col_sel2:
            st.markdown("<br>", unsafe_allow_html=True)
            comparar = st.checkbox("🆚 Comparar", key="ck_comparar")
            
        with col_sel3:
            if comparar:
                opcoes_comparar_ids = [pid for pid in lista_player_ids if pid != jogador_selecionado_id]
                jogador_comparar_id = st.selectbox(
                    "Comparar com:", 
                    opcoes_comparar_ids, 
                    format_func=lambda pid: dict_jogadores.get(pid, str(pid)),
                    key="sel_player_compare"
                )
                jogador_comparar = dict_jogadores.get(jogador_comparar_id, "")
            else:
                jogador_comparar_id = None
                jogador_comparar = None
                st.markdown("<br><span style='color:#555'>Marque ✅ para comparar</span>", unsafe_allow_html=True)

        # --- Função auxiliar para preparar dados de um jogador ---
        def preparar_dados_jogador(id_jogador):
            # Agora filtramos pelo ID único!
            df_j = df[df["playerId"] == id_jogador].copy()
            # Ordenar cronologicamente pela data do torneio
            if "tournamentDate" in df_j.columns:
                df_j = df_j.sort_values("tournamentDate")
            df_evo = df_j.groupby("tournamentFullName", sort=False).agg({
                "kills": "sum", "assists": "sum", "damageDealt": "sum",
                "gamesPlayed": "sum", "tournamentDate": "first",
            }).reset_index()
            df_evo = df_evo.sort_values("tournamentDate").reset_index(drop=True)
            df_evo["KPR"] = (df_evo["kills"] / df_evo["gamesPlayed"]).round(2)
            df_evo["APR"] = (df_evo["assists"] / df_evo["gamesPlayed"]).round(2)
            df_evo["DPR"] = (df_evo["damageDealt"] / df_evo["gamesPlayed"]).round(0)
            # Label legível: "NOME (DD/MM)"
            df_evo["etapa_label"] = df_evo["tournamentFullName"].apply(
                lambda x: x if len(x) <= 40 else x[:37] + "..."
            )
            return df_j, df_evo

        if jogador_selecionado_id:
            df_jogador, df_evolucao = preparar_dados_jogador(jogador_selecionado_id)

            if comparar:
                df_jogador2, df_evolucao2 = preparar_dados_jogador(jogador_comparar_id)

            # --- MÉTRICAS CONSOLIDADAS ---
            total_partidas = int(df_jogador["gamesPlayed"].sum())
            total_kills = int(df_jogador["kills"].sum())
            total_assists = int(df_jogador["assists"].sum())
            total_dano = int(df_jogador["damageDealt"].sum())
            avg_kpr = round(total_kills / total_partidas, 2) if total_partidas > 0 else 0
            avg_apr = round(total_assists / total_partidas, 2) if total_partidas > 0 else 0
            avg_dpr = round(total_dano / total_partidas, 0) if total_partidas > 0 else 0

            if comparar:
                tp2 = int(df_jogador2["gamesPlayed"].sum())
                tk2 = int(df_jogador2["kills"].sum())
                ta2 = int(df_jogador2["assists"].sum())
                td2 = int(df_jogador2["damageDealt"].sum())
                avg_kpr2 = round(tk2 / tp2, 2) if tp2 > 0 else 0
                avg_apr2 = round(ta2 / tp2, 2) if tp2 > 0 else 0
                avg_dpr2 = round(td2 / tp2, 0) if tp2 > 0 else 0

            st.markdown(f"#### 🏅 Resumo — {jogador_selecionado}")
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.metric("🎮 Partidas", total_partidas)
            col2.metric("💀 Kills", total_kills, f"{avg_kpr}/partida")
            col3.metric("🤝 Assists", total_assists, f"{avg_apr}/partida")
            col4.metric("💥 Dano Total", f"{total_dano:,.0f}", f"{avg_dpr:,.0f}/partida")
            col5.metric("📊 Etapas", len(df_evolucao))
            if len(df_evolucao) >= 2:
                delta_kills = int(df_evolucao["kills"].iloc[-1] - df_evolucao["kills"].iloc[-2])
                col6.metric("📈 Tendência Kills", int(df_evolucao["kills"].iloc[-1]), delta_kills)
            else:
                col6.metric("📈 Tendência Kills", total_kills, "—")

            if comparar:
                st.markdown(f"#### 🆚 Resumo — {jogador_comparar}")
                c1, c2, c3, c4, c5, c6 = st.columns(6)
                c1.metric("🎮 Partidas", tp2)
                c2.metric("💀 Kills", tk2, f"{avg_kpr2}/partida")
                c3.metric("🤝 Assists", ta2, f"{avg_apr2}/partida")
                c4.metric("💥 Dano Total", f"{td2:,.0f}", f"{avg_dpr2:,.0f}/partida")
                c5.metric("📊 Etapas", len(df_evolucao2))
                if len(df_evolucao2) >= 2:
                    dk2 = int(df_evolucao2["kills"].iloc[-1] - df_evolucao2["kills"].iloc[-2])
                    c6.metric("📈 Tendência Kills", int(df_evolucao2["kills"].iloc[-1]), dk2)
                else:
                    c6.metric("📈 Tendência Kills", tk2, "—")

            st.markdown("---")
            st.markdown("#### 📊 Evolução por Etapa")

            # Layout helper para criar gráficos de um jogador
            def _chart_layout(title, height=380):
                return dict(
                    title=title,
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white"),
                    margin=dict(l=20, r=20, t=50, b=90), height=height,
                    xaxis=dict(tickangle=-25),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                )

            def criar_graficos_jogador(df_evo, nome, cor_kills="#E31B23", cor_assists="#A91012", cor_dano="Reds"):
                """Cria os 3 gráficos (kills+assists, dano, médias) para um jogador"""
                # 1) Kills & Assists
                fig_ka = go.Figure()
                fig_ka.add_trace(go.Bar(
                    x=df_evo["etapa_label"], y=df_evo["kills"], name="Kills",
                    marker_color=cor_kills, text=df_evo["kills"], textposition="outside",
                    hovertext=df_evo["tournamentFullName"],
                    hovertemplate="<b>%{hovertext}</b><br>Kills: %{y}<extra></extra>",
                ))
                fig_ka.add_trace(go.Bar(
                    x=df_evo["etapa_label"], y=df_evo["assists"], name="Assists",
                    marker_color=cor_assists, text=df_evo["assists"], textposition="outside",
                    hovertext=df_evo["tournamentFullName"],
                    hovertemplate="<b>%{hovertext}</b><br>Assists: %{y}<extra></extra>",
                ))
                fig_ka.update_layout(**_chart_layout(f"Kills & Assists — {nome}"), barmode="group")

                # 2) Dano
                fig_d = go.Figure()
                fig_d.add_trace(go.Bar(
                    x=df_evo["etapa_label"], y=df_evo["damageDealt"], name="Dano",
                    marker=dict(color=df_evo["damageDealt"], colorscale=cor_dano, showscale=False),
                    text=df_evo["damageDealt"].apply(lambda x: f"{x:,.0f}"), textposition="outside",
                    hovertext=df_evo["tournamentFullName"],
                    hovertemplate="<b>%{hovertext}</b><br>Dano: %{y:,.0f}<extra></extra>",
                ))
                fig_d.update_layout(**_chart_layout(f"Dano Total — {nome}"), showlegend=False)

                # 3) Médias KPR + APR
                fig_m = go.Figure()
                fig_m.add_trace(go.Scatter(
                    x=df_evo["etapa_label"], y=df_evo["KPR"], name="Kills/P",
                    mode="lines+markers+text", text=df_evo["KPR"], textposition="top center",
                    line=dict(color=cor_kills, width=3), marker=dict(size=10),
                    hovertext=df_evo["tournamentFullName"],
                    hovertemplate="<b>%{hovertext}</b><br>KPR: %{y:.2f}<extra></extra>",
                ))
                fig_m.add_trace(go.Scatter(
                    x=df_evo["etapa_label"], y=df_evo["APR"], name="Assists/P",
                    mode="lines+markers+text", text=df_evo["APR"], textposition="bottom center",
                    line=dict(color=cor_assists, width=3), marker=dict(size=10),
                    hovertext=df_evo["tournamentFullName"],
                    hovertemplate="<b>%{hovertext}</b><br>APR: %{y:.2f}<extra></extra>",
                ))
                fig_m.update_layout(**_chart_layout(f"Médias por Partida — {nome}"))

                return fig_ka, fig_d, fig_m

            if not comparar:
                # ---------- MODO SOLO: 2 colunas ----------
                fig_ka, fig_d, fig_m = criar_graficos_jogador(df_evolucao, jogador_selecionado)

                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    st.plotly_chart(fig_ka, use_container_width=True)
                with col_g2:
                    st.plotly_chart(fig_d, use_container_width=True)

                col_g3, col_g4 = st.columns(2)
                with col_g3:
                    st.plotly_chart(fig_m, use_container_width=True)
            else:
                # ---------- MODO COMPARAÇÃO: cada jogador na sua coluna ----------
                st.markdown(f"##### 🔴 {jogador_selecionado}  vs  ⚪ {jogador_comparar}")

                fig_ka1, fig_d1, fig_m1 = criar_graficos_jogador(
                    df_evolucao, jogador_selecionado,
                    cor_kills="#E31B23", cor_assists="#A91012", cor_dano="Reds"
                )
                fig_ka2, fig_d2, fig_m2 = criar_graficos_jogador(
                    df_evolucao2, jogador_comparar,
                    cor_kills="#FFFFFF", cor_assists="#777777", cor_dano="Greys"
                )

                col_a, col_b = st.columns(2)
                with col_a:
                    st.plotly_chart(fig_ka1, use_container_width=True)
                with col_b:
                    st.plotly_chart(fig_ka2, use_container_width=True)

                col_c, col_d = st.columns(2)
                with col_c:
                    st.plotly_chart(fig_d1, use_container_width=True)
                with col_d:
                    st.plotly_chart(fig_d2, use_container_width=True)

                col_e, col_f = st.columns(2)
                with col_e:
                    st.plotly_chart(fig_m1, use_container_width=True)
                with col_f:
                    st.plotly_chart(fig_m2, use_container_width=True)

            # --- RADAR ---
            if not comparar:
                # Radar solo fica ao lado do gráfico de médias
                with col_g4:
                    categorias = ["Kills/P", "Assists/P", "Dano/P (÷100)"]
                    valores = [avg_kpr, avg_apr, avg_dpr / 100]
                    fig_radar = go.Figure()
                    fig_radar.add_trace(go.Scatterpolar(
                        r=valores + [valores[0]],
                        theta=categorias + [categorias[0]],
                        fill="toself",
                        fillcolor="rgba(227, 27, 35, 0.25)",
                        line=dict(color="#E31B23", width=2),
                        marker=dict(size=8),
                        name=jogador_selecionado,
                    ))
                    fig_radar.update_layout(
                        title=f"Perfil — {jogador_selecionado}",
                        polar=dict(
                            bgcolor="rgba(0,0,0,0)",
                            radialaxis=dict(visible=True, gridcolor="rgba(255,255,255,0.15)"),
                            angularaxis=dict(gridcolor="rgba(255,255,255,0.15)"),
                        ),
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="white"),
                        margin=dict(l=40, r=40, t=60, b=40), height=380,
                        showlegend=False,
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)
            else:
                # Radar comparativo centralizado
                st.markdown("---")
                st.markdown("#### 🎯 Comparação de Perfil")
                _, col_radar, _ = st.columns([1, 2, 1])
                with col_radar:
                    categorias = ["Kills/P", "Assists/P", "Dano/P (÷100)"]
                    valores = [avg_kpr, avg_apr, avg_dpr / 100]
                    valores2 = [avg_kpr2, avg_apr2, avg_dpr2 / 100]
                    fig_radar = go.Figure()
                    fig_radar.add_trace(go.Scatterpolar(
                        r=valores + [valores[0]],
                        theta=categorias + [categorias[0]],
                        fill="toself",
                        fillcolor="rgba(227, 27, 35, 0.3)",
                        line=dict(color="#E31B23", width=2),
                        marker=dict(size=8),
                        name=jogador_selecionado,
                    ))
                    fig_radar.add_trace(go.Scatterpolar(
                        r=valores2 + [valores2[0]],
                        theta=categorias + [categorias[0]],
                        fill="toself",
                        fillcolor="rgba(255, 255, 255, 0.15)",
                        line=dict(color="#FFFFFF", width=2),
                        marker=dict(size=8),
                        name=jogador_comparar,
                    ))
                    fig_radar.update_layout(
                        title=f"Perfil — {jogador_selecionado} vs {jogador_comparar}",
                        polar=dict(
                            bgcolor="rgba(0,0,0,0)",
                            radialaxis=dict(visible=True, gridcolor="rgba(255,255,255,0.15)"),
                            angularaxis=dict(gridcolor="rgba(255,255,255,0.15)"),
                        ),
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="white"),
                        margin=dict(l=40, r=40, t=60, b=40), height=420,
                        showlegend=True,
                        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)

            # --- TABELA DETALHADA ---
            st.markdown("---")
            st.markdown("#### 📋 Detalhamento por Etapa")
            
            if comparar:
                st.markdown(f"##### 🔴 Jogador Principal: {jogador_selecionado}")
            else:
                st.markdown(f"##### 👤 {jogador_selecionado}")
                
            df_tabela = df_evolucao[["tournamentFullName", "tournamentDate", "gamesPlayed", "kills", "assists", "damageDealt", "KPR", "APR", "DPR"]].copy()
            df_tabela["tournamentDate"] = df_tabela["tournamentDate"].dt.strftime("%d/%m/%Y")
            df_tabela.columns = ["Etapa", "Data", "Partidas", "Kills", "Assists", "Dano", "Kills/P", "Assists/P", "Dano/P"]

            st.dataframe(
                df_tabela.style
                    .background_gradient(subset=["Kills"], cmap="Reds", vmin=0)
                    .background_gradient(subset=["Dano"], cmap="YlOrRd", vmin=0)
                    .format({"Kills/P": "{:.2f}", "Assists/P": "{:.2f}", "Dano/P": "{:.0f}"}),
                use_container_width=True,
                hide_index=True,
            )

            if comparar:
                st.markdown(f"##### ⚪ Comparação: {jogador_comparar}")
                df_tab2 = df_evolucao2[["tournamentFullName", "tournamentDate", "gamesPlayed", "kills", "assists", "damageDealt", "KPR", "APR", "DPR"]].copy()
                df_tab2["tournamentDate"] = df_tab2["tournamentDate"].dt.strftime("%d/%m/%Y")
                df_tab2.columns = ["Etapa", "Data", "Partidas", "Kills", "Assists", "Dano", "Kills/P", "Assists/P", "Dano/P"]
                st.dataframe(
                    df_tab2.style
                        .background_gradient(subset=["Kills"], cmap="Greys", vmin=0)
                        .background_gradient(subset=["Dano"], cmap="Greys", vmin=0)
                        .format({"Kills/P": "{:.2f}", "Assists/P": "{:.2f}", "Dano/P": "{:.0f}"}),
                    use_container_width=True,
                    hide_index=True,
                )

    # --- CONTEÚDO DA ABA 3 ---
    with aba3:
        st.subheader("🔍 Resultados Oficiais da Etapa (com Kill Cap)")

        etapa_escolhida = st.selectbox(
            "Selecione a etapa:",
            st.session_state.etapas_processadas,
            key="seletor_aba3"
        )

        if etapa_escolhida:
            t_id_escolhido = st.session_state.dicionario_etapas[etapa_escolhida]

            # --- FONTE 1: HTML do site (scores oficiais com kill cap) ---
            html_scores = get_html_scores(t_id_escolhido)

            # --- FONTE 2: API (dados complementares: dano, assists, jogadores) ---
            scores_etapa = get_scores(t_id_escolhido)

            if not html_scores and (not scores_etapa or "teamData" not in scores_etapa):
                st.warning("Nenhum dado encontrado para a etapa selecionada.")
            else:
                # Monta dicionario de dados da API por time
                api_por_time = {}
                jogadores_etapa = []

                if scores_etapa and "teamData" in scores_etapa:
                    for team in scores_etapa["teamData"]:
                        tname = team.get("teamName", "")
                        api_por_time[tname] = {
                            "kills_raw":   team.get("kills", 0),
                            "dano":        team.get("damageDealt", 0),
                            "assists":     team.get("assists", 0),
                            "partidas":    len(team.get("ranking", [])),
                            "ranking":     team.get("ranking", []),
                        }
                        if "playersData" in team:
                            for p in team["playersData"]:
                                jogadores_etapa.append({
                                    "Time":    tname,
                                    "Jogador": p.get("playerName", "?"),
                                    "Kills":   p.get("kills", 0),
                                    "Assists": p.get("assists", 0),
                                    "Dano":    p.get("damageDealt", 0),
                                    "Partidas": p.get("gamesPlayed", 0),
                                })

                # Monta tabela final
                times_lista = []

                if html_scores:
                    # MODO PRINCIPAL: usa pontos do HTML (kill cap aplicado)
                    for tname, hdata in html_scores.items():
                        api = api_por_time.get(tname, {})
                        times_lista.append({
                            "Time":            tname,
                            "Pontos Oficiais": hdata["score"],
                            "Kills (raw)":     hdata["kills_raw"],
                            "Partidas":        api.get("partidas", "-"),
                            "Dano Total":      api.get("dano", 0),
                            "_fonte":          "site",
                        })
                    fonte_label = "✅ Pontos oficiais do site (Kill Cap de 10 já aplicado)"
                    st.success(fonte_label)
                else:
                    # FALLBACK: usa pontos da API (sem kill cap)
                    for tname, api in api_por_time.items():
                        times_lista.append({
                            "Time":            tname,
                            "Pontos Oficiais": api.get("kills_raw", 0),  # placeholder
                            "Kills (raw)":     api.get("kills_raw", 0),
                            "Partidas":        api.get("partidas", 0),
                            "Dano Total":      api.get("dano", 0),
                            "_fonte":          "api",
                        })
                    st.warning(
                        "⚠️ Página de resultados não disponível para esta etapa. "
                        "Exibindo dados brutos da API (sem Kill Cap aplicado)."
                    )

                if times_lista:
                    df_times = pd.DataFrame(times_lista).sort_values(
                        by="Pontos Oficiais", ascending=False
                    ).reset_index(drop=True)
                    df_times.index += 1

                    cols_vis = [c for c in df_times.columns if not c.startswith("_")]
                    df_vis = df_times[cols_vis]

                    col_t, col_j = st.columns(2)

                    with col_t:
                        st.markdown("#### 🏆 Ranking de Equipes")
                        st.dataframe(
                            df_vis.style.background_gradient(
                                subset=["Pontos Oficiais"], cmap="Greens"
                            ),
                            use_container_width=True
                        )

                    with col_j:
                        st.markdown("#### 🥇 Destaques Individuais")
                        if jogadores_etapa:
                            df_j = pd.DataFrame(jogadores_etapa).sort_values(
                                by=["Kills", "Dano"], ascending=[False, False]
                            ).reset_index(drop=True)
                            df_j.index += 1
                            st.dataframe(
                                df_j.style.background_gradient(
                                    subset=["Kills"], cmap="Blues"
                                ),
                                use_container_width=True
                            )
                        else:
                            st.info("Dados individuais não disponíveis para esta etapa.")

    # --- CONTEÚDO DA ABA 4 (CSI ARENA) ---
    with aba4:
        st.subheader("🕵️‍♂️ CSI Arena: Investigação de Contas (Anti-Smurf)")
        st.markdown("Esta seção agrupa todas as métricas detalhadas de um único Player ID para expor saltos de performance entre múltiplos nicknames da mesma pessoa.")
        
        # Lista iterável de IDs com seu nick mais recente
        df_sorted_csi = df.sort_values(by="tournamentDate", ascending=True)
        # Mapeia ID -> Último Nick
        id_to_nick = df_sorted_csi.groupby("playerId")["playerName"].last().to_dict()
        opcoes_csi = [f"{pid} ({nick})" for pid, nick in id_to_nick.items()]
        # Ordena a UI alfabeticamente pelo primeiro caractere do nick
        opcoes_csi.sort(key=lambda x: str(x.split("(")[1]).lower() if "(" in x else "")
        
        id_selecionado_raw = st.selectbox("Selecione a conta para investigar as ocorrências:", opcoes_csi)
        
        if id_selecionado_raw:
            pid = id_selecionado_raw.split(" (")[0]
            nick_principal = id_to_nick[pid]
            df_pid = df_sorted_csi[df_sorted_csi["playerId"] == pid]
            
            nicks_usados = df_pid["playerName"].unique()
            
            st.markdown(f"### Dossiê Investigativo: `{pid}`")
            col_id1, col_id2 = st.columns(2)
            col_id1.metric("Nickname Reconhecido (Último)", nick_principal)
            col_id2.metric("Volume Falso (Nomes Únicos)", len(nicks_usados))
            
            st.markdown("#### 🃏 Disparidade de Performance (Por Identidade)")
            st.write("Verifique se as estatísticas abaixo flutuam massivamente quando a pessoa troca de nome:")
            # Agrupar dados POR NOME DE JOGADOR dentro do ID
            df_csi_nicks = df_pid.groupby("playerName").agg({
                "tournamentFullName": "nunique",
                "gamesPlayed": "sum",
                "kills": "sum",
                "damageDealt": "sum"
            }).reset_index()
            
            df_csi_nicks.columns = ["Nickname Utilizado", "Etapas Disputadas", "Partidas", "Kills Totais", "Dano Total"]
            df_csi_nicks["Kills / P"] = (df_csi_nicks["Kills Totais"] / df_csi_nicks["Partidas"]).round(2)
            df_csi_nicks["Dano / P"] = (df_csi_nicks["Dano Total"] / df_csi_nicks["Partidas"]).round(0)
            
            st.dataframe(
                df_csi_nicks.style.background_gradient(subset=["Kills / P", "Dano / P"], cmap="Reds"),
                use_container_width=True
            )
            
            st.markdown("#### 📅 Ficha Corrida (Cronologia)")
            df_cronologia = df_pid[["tournamentDate", "tournamentFullName", "playerName", "kills", "damageDealt"]].copy()
            df_cronologia = df_cronologia.sort_values(by="tournamentDate", ascending=False)
            df_cronologia["tournamentDate"] = df_cronologia["tournamentDate"].dt.strftime("%d/%m/%Y")
            df_cronologia.columns = ["Data", "Competição", "Nickname Utilizado", "Kills Obtidas", "Dano Causado"]
            
            st.dataframe(df_cronologia, use_container_width=True)
            
            if len(nicks_usados) > 1:
                st.warning("⚠️ **ALERTA CSI:** Esta conta já entrou nos lobbies disfarçada sob nomes falsos distintos. Verifique a tabela de disparidade para detectar indícios de adulteração de skill!")
