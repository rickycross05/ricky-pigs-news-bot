def parse_and_filter(raw_articles, keywords=None):
    """Pulisce i dati grezzi e filtra in base alle keyword."""
    clean_articles = []
    
    # tutte le keyword in minuscolo per un confronto accurato
    if keywords:
        keywords = [k.lower() for k in keywords]
        
    for article in raw_articles:
        # Estraiamo i campi essenziali (usando .get per evitare errori se mancano)
        title = article.get("title", "Senza Titolo")
        link = article.get("link", "#")
        # I feed RSS possono usare 'published' o 'updated' per la data
        date = article.get("published", article.get("updated", "Data sconosciuta"))
        source = article.get("source_name", "Fonte sconosciuta")
        
        # Logica di filtraggio
        if keywords:
            title_lower = title.lower()
            # Se NESSUNA keyword è presente nel titolo, saltiamo l'articolo (continue)
            if not any(k in title_lower for k in keywords):
                continue
                
        # Se supera il filtro, creiamo un oggetto pulito e lo salviamo
        clean_articles.append({
            "title": title,
            "link": link,
            "date": date,
            "source": source
        })
        
    return clean_articles