import requests
from lxml import html

class RequestsSite:
        
    def get_html(self, url):
        self.html = requests.get(url)

    def save_html(self, html, filename):
        self.html = html
        
    