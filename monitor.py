import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- 1. CONFIGURAZIONE SICURA ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ ERRORE: Chiave API non trovata.")
    exit()

# Inizializzazione Client (Nuova SDK)
client = genai.Client(api_key=api_key)

# --- 2. MODULO INTELLIGENCE (RACCOLTA DATI) ---
def scarica_hacker_news():
    print("📡 Collegamento al satellite (Scraping https://news.ycombinator.com/)...")
    try:
        response = requests.get("https://news.ycombinator.com/", timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Estrai i titoli
        titoli = []
        news_items = soup.find_all("span", class_="titleline")
        for item in news_items[:15]: # Prendiamo i primi 15 top trend
            titoli.append(item.get_text())
            
        print(f"✅ Intercettati {len(titoli)} segnali dal web.")
        return "\n".join(titoli)
    except Exception as e:
        print(f"❌ Errore durante lo scraping: {e}")
        return None

# --- 3. MODULO ANALISI (GEMINI 2.0) ---
def analizza_segnali(testo_input):
    print("\n🧠 Avvio Analisi Intelligence (Gemini 2.0)...")
    
    prompt = f"""
    Agisci come un analista di intelligence tecnologica di alto livello.
    Analizza questi titoli presi ora da Hacker News:
    
    {testo_input}
    
    OUTPUT RICHIESTO:
    1. Identifica il "Trend Dominante" in una frase.
    2. Evidenzia 3 notizie critiche che potrebbero avere impatto sul mercato o sulla tecnologia.
    3. Usa un tono professionale, sintetico e diretto (in Italiano).
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ Errore AI: {e}"

# --- 4. ESECUZIONE ---
if __name__ == "__main__":
    raw_data = scarica_hacker_news()
    
    if raw_data:
        report = analizza_segnali(raw_data)
        print("\n" + "="*40)
        print("📄 REPORT INTELLIGENCE")
        print("="*40)
        print(report)
        print("="*40)
    else:
        print("⚠️ Nessun dato da analizzare.")
    