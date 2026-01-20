import streamlit as st
import time
from monitor import scarica_hacker_news, analizza_segnali

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="AI Tech Intelligence",
    page_icon="📡",
    layout="centered"
)

# --- HEADER ---
st.title("📡 AI Web Intelligence Unit")
st.caption("Monitoring Real-Time Tech Signals via Hacker News & Gemini 2.0")

# --- SIDEBAR (CONTROLLI) ---
with st.sidebar:
    st.header("🎮 Controlli")
    if st.button("Avvia Scansione", type="primary"):
        start_scan = True
    else:
        start_scan = False
    
    st.divider()
    st.markdown("**Stato Sistema:** 🟢 Operativo")
    st.markdown("**Modello:** Gemini 2.0 Flash")

# --- LOGICA APPLICAZIONE ---
if start_scan:
    # 1. Scraping
    with st.status("Intercettazione segnali in corso...", expanded=True) as status:
        st.write("Connessione a news.ycombinator.com...")
        time.sleep(1) # Effetto scenico
        raw_data = scarica_hacker_news()
        
        if raw_data:
            st.write("✅ Segnali acquisiti.")
            st.write("🧠 Invio dati al Neural Engine (Gemini)...")
            status.update(label="Analisi completata!", state="complete", expanded=False)
        else:
            status.update(label="Errore connessione", state="error")
            st.stop()

    # 2. Visualizzazione Report
    st.divider()
    st.subheader("📄 Rapporto Strategico")
    
    with st.spinner("Generazione insight..."):
        report = analizza_segnali(raw_data)
        
    # Visualizziamo il report in un bel box
    st.markdown(report)
    
    # 3. Dati Grezzi (Espandibile)
    with st.expander("🔍 Vedi dati grezzi (Titoli intercettati)"):
        st.text(raw_data)

else:
    st.info("Premi 'Avvia Scansione' nella barra laterale per attivare l'agente.")

# Footer
st.markdown("---")
st.markdown("*Sistema sviluppato da Giacomo | Powered by Google GenAI*")