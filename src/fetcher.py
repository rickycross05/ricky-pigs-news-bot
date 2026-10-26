import json
import feedparser
import requests
from bs4 import BeautifulSoup

def load_sources(config_path="config/sources.json"):
    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)

def fetch_rss_feeds(sources):
    raw_articles = []
    for feed in sources.get("rss_feeds", []):
        print(f"Scaricando RSS da: {feed['name']}...")
        parsed_feed = feedparser.parse(feed["url"])
        for entry in parsed_feed.entries:
            entry['source_name'] = feed['name']
            raw_articles.append(entry)
    return raw_articles

def fetch_scraped_pages(sources):
    """Estrae titoli e link cercando tutti i link lunghi."""
    raw_articles = []
    
    # Aggiungiamo più dettagli per sembrare un vero browser su macOS
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    for page in sources.get("scrape_pages", []):
        print(f"Eseguendo scraping su: {page['name']}...")
        try:
            response = requests.get(page["url"], headers=headers)
            
            if response.status_code != 200:
                print(f"⚠️ Accesso negato su {page['name']} (Codice {response.status_code})")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # cerchiamo TUTTI i tag <a> (i link)
            for link_tag in soup.find_all('a', href=True):
                title = link_tag.get_text(strip=True)
                link = link_tag['href']
                
                # Un titolo di una notizia è solitamente lungo.
                # Evitiamo link come "Home", "Contatti", "Login", o piccole etichette
                if len(title) > 25 and title.count(' ') > 4:
                    
                    if link.startswith('/'):
                        # Trasformiamo i link relativi in link assoluti (completi)
                        base_url = "https://www.3tres3.com" if "3tres3" in page['name'].lower() else page["url"]
                        link = f"{base_url}{link}"
                        
                    raw_articles.append({
                        "title": title,
                        "link": link,
                        "published": "Oggi (Scraping)",
                        "source_name": page['name']
                    })
                    
        except Exception as e:
            print(f"Errore di connessione su {page['name']}: {e}")
            
    # Lo scraping brutale spesso pesca lo stesso link due volte (es. sull'immagine e sul testo).
    # Qui puliamo i duplicati prima di mandarli al parser.
    unique_articles = []
    seen_links = set()
    for art in raw_articles:
        if art['link'] not in seen_links:
            unique_articles.append(art)
            seen_links.add(art['link'])
            
    return unique_articles