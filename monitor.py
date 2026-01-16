import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv

# --- CONFIGURAZIONE ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("ERRORE: Chiave API mancante nel file .env")
    exit()

genai.configure(api_key=api_key)

def scarica_news_tech():
    """Scarica i titoli in tempo reale da Hacker News."""
    url = "https://news.ycombinator.com/"
    print(f"--- 📡 Collegamento al satellite (Scraping {url})... ---")
    
    try:
        # 1. Chiamata al sito
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Errore connessione: {response.status_code}")
            return []
        
        # 2. Pulizia HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. Estrazione Titoli (Hacker News usa la classe 'titleline')
        titoli = []
        elementi = soup.find_all(class_='titleline')
        
        for el in elementi:
            titolo_pulito = el.get_text()
            titoli.append(titolo_pulito)
            
        print(f"✅ Intercettati {len(titoli)} segnali dal web.")
        return titoli[:40] # Prendiamo i primi 40 titoli

    except Exception as e:
        print(f"❌ Errore nello scraping: {e}")
        return []

def analista_ai(lista_titoli):
    """Usa Gemini per filtrare il rumore e trovare opportunità."""
    print("\n--- 🧠 Avvio Analisi Intelligence (Gemini 2.0) ---")
    
    # Creiamo un blocco di testo unico da inviare all'AI
    testo_grezzo = "\n".join([f"- {t}" for t in lista_titoli])
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""
    Sei un Analista di Strategia Industriale.
    Ho scaricato questi titoli dal web in tempo reale.
    
    LISTA NEWS:
    {testo_grezzo}
    
    OBIETTIVO:
    Identifica SE ci sono notizie riguardanti:
    1. ENERGIA (Nucleare, Rinnovabili, Batterie, Oil&Gas)
    2. INTELLIGENZA ARTIFICIALE applicata (non gossip, ma nuovi modelli o strumenti)
    3. HARDWARE (Chip, Processori, Robotica)
    
    OUTPUT RICHIESTO:
    Se trovi notizie rilevanti, elencale e spiega in una frase perché sono strategiche.
    Se NON trovi nulla di specifico, dimmi qual è il "Trend del Giorno" (di cosa parlano tutti?).
    """
    
    try:
        response = model.generate_content(prompt)
        print("\n" + "="*50)
        print("📊 REPORT INTELLIGENCE DI MERCATO")
        print("="*50)
        print(response.text)
    except Exception as e:
        print(f"Errore AI: {e}")

if __name__ == "__main__":
    # Esecuzione sequenziale
    notizie = scarica_news_tech()
    if notizie:
        analista_ai(notizie)