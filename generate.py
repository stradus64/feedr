import feedparser
from datetime import datetime
import os
from html import escape

def parse_feeds(file_path):
    entries = []
    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    for url in urls:
        feed = feedparser.parse(url)
        feed_title = feed.feed.get('title', 'Unknown Feed')
        for entry in feed.entries:
            title = entry.get('title', 'No Title')
            link = entry.get('link', '#')
            published = entry.get('published', '')
            date = ''
            if published:
                date = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%dT%H:%M')
            entries.append({
                'title': title,
                'link': link,
                'date': date,
                'feed_title': feed_title
            })
    return sorted(entries, key=lambda x: x['date'].lower(), reverse=True)

def generate_html(entries, output_file='index.html'):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n')
        f.write('<link rel="stylesheet" href="sakura.css" media="screen" />\n')
        f.write('<link rel="stylesheet" href="sakura-dark.css" media="screen and (prefers-color-scheme: dark)" />\n')
        f.write('<title>RSS Feed Entries</title>\n</head>\n<body>\n')
        f.write('<h1>RSS Feed Entries</h1>\n<ul>\n')
        for entry in entries:
            f.write(f"<li id='{entry['date']}'> <a href='#{entry['date']}'> ({entry['date']}) </a>"
                    f"<a href='{escape(entry['link'])}'><strong>{escape(entry['title'])}</strong></a> – <em>{escape(entry['feed_title'])}</em></li>\n")
        f.write('</ul>\n</body>\n</html>')

if __name__ == "__main__":
    rss_file = os.path.join(os.path.dirname(__file__), 'rss.txt')
    entries = parse_feeds(rss_file)
    generate_html(entries)
    print("HTML file 'index.html' has been created.")
