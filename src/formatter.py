import html

def format_as_text(articles):
    """Formatta gli articoli come HTML sicuro (ideale per Telegram)."""
    if not articles:
        return "Nessuna nuova notizia corrispondente ai tuoi criteri oggi."
    
    # Usiamo i tag <b> invece dei doppi asterischi
    report = "📰 <b>IL TUO REPORT QUOTIDIANO</b> 📰\n\n"
    
    sources = set([a['source'] for a in articles])
    
    for source in sources:
        report += f"🔹 <b>{html.escape(source)}</b>\n"
        source_articles = [a for a in articles if a['source'] == source]
        
        for article in source_articles:
            # html.escape rende innocui eventuali simboli < o > o & presenti nei titoli
            safe_title = html.escape(article['title'])
            report += f"• {safe_title}\n  🔗 {article['link']}\n"
            
        report += "\n"
        
    return report

def format_as_html(articles):
    """Formatta gli articoli in HTML base (ideale per Email)."""
    if not articles:
        return "Nessuna nuova notizia corrispondente ai tuoi criteri oggi."
    
    html = '📰 Il Tuo Report Quotidiano 📰\n'
    
    sources = set([a['source'] for a in articles])
    
    for source in sources:
        html += f"🔹 {source}\n\n"
        source_articles = [a for a in articles if a['source'] == source]
        for article in source_articles:
            html += f"  {article['title']}\n"
            html += f"  Leggi di più\n"
        html += "\n\n"
        
    return html