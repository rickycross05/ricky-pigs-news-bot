import os
import time
from html import escape
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def send_telegram_message(text_report):
    """Invia il report a Telegram, suddividendolo per righe per non rompere il Markdown."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("Errore: Credenziali Telegram mancanti nel file .env!")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # Il limite di Telegram è 4096.
    MAX_LENGTH = 4000
    
    chunks = []
    current_chunk = ""
    
    # Dividiamo l'intero report riga per riga
    for line in text_report.split('\n'):
        # Se aggiungendo la prossima riga superiamo il limite, salviamo il pacchetto e ripartiamo
        if len(current_chunk) + len(line) + 1 > MAX_LENGTH:
            chunks.append(current_chunk)
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"
            
    # Ricordiamoci di aggiungere l'ultimo pezzo rimasto
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    success = True
    
    for i, chunk in enumerate(chunks):
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        
        try:
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                print(f"📩 Parte {i+1} di {len(chunks)} inviata con successo!")
            else:
                print(f"Errore nell'invio della parte {i+1}: {response.text}")
                success = False
                
        except Exception as e:
            print(f"Errore di connessione a Telegram: {e}")
            success = False
            
        # Pausa per non attivare l'antispam
        time.sleep(1)
        
    return success