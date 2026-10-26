from src.fetcher import load_sources, fetch_rss_feeds, fetch_scraped_pages
from src.parser import parse_and_filter
from src.formatter import format_as_text, format_as_html
from src.notifier import send_telegram_message

def main():
    print("Avvio Aggregatore di Notizie...\n")
    
    # 1. Carichiamo le fonti
    print("fase 1: caricamento fonti")
    config = load_sources()
    sources = config
    keywords = config.get("keywords", [])
    
    # 2. Scarichiamo le notizie
    print("fase 2: download dati")
    raw_rss = fetch_rss_feeds(config)
    raw_scraped = fetch_scraped_pages(config)
    raw_articles = raw_rss + raw_scraped
    
    print(f"\nOperazione completata: scaricati {len(raw_articles)} articoli in totale.")
    
    # 3. pulizia e filtraggio
    print("fase 3: pulizia e filtraggio")
    clean_articles = parse_and_filter(raw_articles, config.get("keywords", []))
    
    print(f"\nOperazione completata: trovati {len(clean_articles)} articoli interessanti su {len(raw_articles)}.")
    
    # 4. formattazione
    print("fase 4: formattazione")
    text_report = format_as_text(clean_articles)
    html_report = format_as_html(clean_articles)
    
    # Salviamo il report di testo (anteprima Telegram/Console)
    with open("preview_report.txt", "w", encoding="utf-8") as f:
        f.write(text_report)
        
    # Salviamo il report HTML (anteprima Email)
    with open("preview_report.html", "w", encoding="utf-8") as f:
        f.write(html_report)
    
    print("\n✅ Generazione completata!")
    
    # 5. invio dati
    print("fase 4: invio dati su telegram")
    send_telegram_message(text_report)
    
    

if __name__ == "__main__":
    main()