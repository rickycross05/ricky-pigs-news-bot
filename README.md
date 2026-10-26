# 🐷 Ricky Pigs News - Telegram Automation Bot

Un bot Telegram automatizzato, sviluppato in Python, progettato per aggregare, filtrare e distribuire in tempo reale gli aggiornamenti e le notizie del mercato suinicolo italiano e internazionale.

L'obiettivo del progetto è ottimizzare il flusso di informazioni per i professionisti del settore zootecnico, automatizzando la lettura dei feed RSS dai principali portali di informazione e mercato.

## ✨ Funzionalità Principali
*   **Aggregazione RSS:** Estrapola automaticamente le ultime notizie dai principali feed del settore (come Informatore Zootecnico, 3tres3, report ISMEA e listini CUN Suini).
*   **Filtraggio Intelligente:** Analizza e seleziona solo gli articoli rilevanti, scartando i rumori di fondo tramite parsing dei testi.
*   **Notifiche Real-Time:** Formatta e inoltra i contenuti direttamente su un canale Telegram dedicato sfruttando le API ufficiali.

## 🛠️ Tecnologie Utilizzate
*   **Linguaggio:** Python
*   **Librerie Core:** `feedparser` (parsing RSS), `beautifulsoup4` (scraping HTML), `requests` (richieste HTTP e invio tramite API Telegram).
*   **Gestione Configurazione:** `python-dotenv` per la gestione sicura dei token.

## 🚀 Come avviare il progetto in locale

1. Clona il repository:
   ```bash git clone https://github.com/rickycross05/ricky-pigs-news-bot.git```
2. Copia il file config/sources.example.json, rinominalo in config/sources.json e inserisci al suo  interno i tuoi feed RSS.