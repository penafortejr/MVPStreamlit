# app.py — Versão simples do SMEL Conectada (sem PDF)
from datetime import date
import io
import pandas as pd
import streamlit as st

# ---------- CONFIG ----------
APP_TITLE = "SMEL Conectada — Protótipo Simples"
SUBTITLE = "Portal acadêmico • Baseado no PDTI da Secretaria de Esporte"

DEFAULT_EVENTS = [
    {"id": 1, "name": "Campeonato Municipal de Futebol", "venue": "Estádio Central", "date": "2025-06-15", "category": "Adulto"},
    {"id": 2, "name": "Circuito Escolar de Atletismo", "venue": "Parque das Águas", "date": "2025-07-20", "category": "Escolar"}
]

# ---------- SESSÃO ----------
if "events" not in st.session_state:
    st.session_state.events = DEFAULT_EVENTS.copy()
if "inscriptions" not in st.session_state:
    st.session_state.inscriptions = []

# ---------- FUNÇÕES ----------
def next_event_id():
    return max([e["id"] for e in st.session_state.events]) + 1 if st.session_state.events else 1

def add_event(name, venue, date_ev, category):
    st.session_state.events.append({
        "id": next_event_id(),
        "name": name,
        "venue": venue,
        "date": date_ev,
        "category": category
    })
    st.success(f"Evento '{name}' criado com sucesso!")

def add_inscription(name, team, event_id, contact):
    event_name = next(e["name"] for e in st.session_state.events if e["id"] == event_id)
    st.session_state.inscriptions.append({
        "id": len(st.session_state.inscriptions) + 1,
        "name": name,
        "team": team,
        "event": event_name,
        "contact": contact,
        "date": date.today().isoformat()
    })
    st.success(f"Inscrição de {name} adicionada com sucesso!")

def df_inscriptions():
    if not st.session_state.inscriptions:
        return pd.DataFrame(columns=["Nome","Equipe","Evento","Contato","Data"])
    df = pd.DataFrame(st.session_state.inscriptions)
    return df.rename(columns={"name":"Nome","team":"Equipe","event":"Evento","contact":"Contato","date":"Data"})

# ---------- ESTILO ----------
st.set_page_config(page_title=APP_TITLE, layout="wide")
st.markdown("""
<style>
:root { --bg:#0b1220; --card:#111827; --muted:#9ca3af; --accent:#06b6d4; --text:#e5e7eb; }
.stApp { background:linear-gradient(180deg,var(--bg),#0f172a); color:var(--text); }
.block-container { padding:1.2rem 2rem; }
.card { background:rgba(255,255,255,0.03); border-radius:10px; padding:1rem; margin-bottom:0.6rem; }
.muted { color:var(--muted); font-size:0.9rem; }
</style>
""", unsafe_allow_html=True)

# ---------- MENU ----------
with st.sidebar:
    st.markdown("## 🧭 Menu")
    page = st.radio("", ["🏠 Início", "🏟️ Eventos", "🧾 Inscrições", "📤 Exportar", "ℹ️ Sobre"])
    st.markdown("---")
    if st.button("🧹 Limpar inscrições"):
        st.session_state.inscriptions = []
        st.info("Inscrições apagadas (sessão atual).")
    if st.button("🔄 Restaurar eventos"):
        st.session_state.events = DEFAULT_EVENTS.copy()
        st.success("Eventos restaurados!")

# ---------- PÁGINAS ----------
if page == "🏠 Início":
    st.title(APP_TITLE)
    st.caption(SUBTITLE)
    st.markdown("---")
    st.subheader("📅 Próximos eventos")
    for ev in st.session_state.events:
        st.markdown(f"<div class='card'><strong>{ev['name']}</strong><div class='muted'>Local: {ev['venue']} • Data: {ev['date']} • Categoria: {ev['category']}</div></div>", unsafe_allow_html=True)

elif page == "🏟️ Eventos":
    st.title("Gerenciar Eventos")
    st.markdown("Crie e visualize eventos esportivos.")
    with st.form("form_event"):
        name = st.text_input("Nome do evento")
        venue = st.text_input("Local / Ginásio")
        date_ev = st.date_input("Data", value=date.today())
        category = st.selectbox("Categoria", ["Geral", "Escolar", "Adulto", "Infantil", "Popular"])
        if st.form_submit_button("Criar evento") and name.strip():
            add_event(name.strip(), venue.strip(), date_ev.isoformat(), category)
    st.markdown("---")
    st.subheader("📋 Eventos atuais")
    df = pd.DataFrame(st.session_state.events)
    st.dataframe(df.rename(columns={"name":"Nome","venue":"Local","date":"Data","category":"Categoria"}), use_container_width=True)

elif page == "🧾 Inscrições":
    st.title("Inscrições")
    if not st.session_state.events:
        st.warning("Crie um evento primeiro.")
    else:
        with st.form("form_insc"):
            name = st.text_input("Nome do participante")
            team = st.text_input("Equipe / Escola")
            ev_choice = st.selectbox("Evento", [(e["id"], e["name"]) for e in st.session_state.events], format_func=lambda x: x[1])
            contact = st.text_input("Contato (telefone ou e-mail)")
            if st.form_submit_button("Salvar inscrição") and name.strip():
                add_inscription(name.strip(), team.strip(), ev_choice[0], contact.strip())
    st.markdown("---")
    st.subheader("📄 Inscrições atuais")
    df = df_inscriptions()
    st.dataframe(df, use_container_width=True)

elif page == "📤 Exportar":
    st.title("Exportar inscrições")
    df = df_inscriptions()
    if df.empty:
        st.info("Nenhuma inscrição para exportar.")
    else:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📄 Baixar CSV", csv, "inscricoes_smel.csv", "text/csv")
        try:
            import xlsxwriter
            to_xlsx = io.BytesIO()
            with pd.ExcelWriter(to_xlsx, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Inscrições")
                writer.close()
            st.download_button("📊 Baixar XLSX", to_xlsx.getvalue(), "inscricoes_smel.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception:
            st.info("Instale o pacote 'xlsxwriter' se quiser exportar XLSX (opcional).")

elif page == "ℹ️ Sobre":
    st.title("Sobre o Projeto")
    st.markdown("""
    Protótipo acadêmico baseado no **PDTI da SMEL**  
    Desenvolvido com **Streamlit** — sem banco de dados.  
    Permite cadastrar eventos, fazer inscrições e exportar dados.
    """)
    st.caption("SMEL Conectada — Trabalho acadêmico 2025")
