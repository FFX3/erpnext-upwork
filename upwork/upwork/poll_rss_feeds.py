import frappe
import feedparser
from bs4 import BeautifulSoup

def process_feed(rss_feed_doc):
    parsed_entries = []
    feed = feedparser.parse(rss_feed_doc.rss_feed)
    for entry in feed.entries:
        soup = BeautifulSoup(entry.content[0].value, 'html.parser')
        content = soup.get_text(separator="\n")
        link = entry.link
        parsed_entries.append({
            'description': content,
            'title': entry.title,
            'url': link
        })
    urls = [entry.get('url') for entry in parsed_entries]
    conflicts = frappe.db.get_list('Upwork RSS Feed Entries', pluck='url', filters={
        'url': ['in', urls]
    })
    entries_pending_processing = []
    for entry in parsed_entries:
        if entry['url'] in conflicts:
            continue
        doc = frappe.new_doc('Upwork RSS Feed Entries')
        doc.title = entry['title']
        doc.url = entry['url']
        doc.description = entry['description']
        doc.insert()

def run():
    rss_feed_docs = frappe.db.get_list('Upwork Job RSS Feeds', fields=['rss_feed', 'name'])
    for rss_feed_doc in rss_feed_docs:
        process_feed(rss_feed_doc)

