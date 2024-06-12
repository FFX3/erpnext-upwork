import frappe
import feedparser
from bs4 import BeautifulSoup

def process_feed(rss_feed_doc):
    feed = feedparser.parse(rss_feed_doc.rss_feed)
    for entry in feed.entries:
        soup = BeautifulSoup(entry.content[0].value, 'html.parser')
        content = soup.get_text(separator="\n")
        link = entry.link
        doc = frappe.new_doc('Upwork RSS Feed Entries')
        doc.title = entry.title
        doc.url = entry.link
        doc.description = content
        doc.insert(ignore_if_duplicate=True)

def run():
    rss_feed_docs = frappe.db.get_list('Upwork Job RSS Feeds', fields=['rss_feed', 'name'])
    for rss_feed_doc in rss_feed_docs:
        process_feed(rss_feed_doc)

