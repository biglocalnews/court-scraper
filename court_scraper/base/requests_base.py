import requests
from lxml import html
from fake_useragent import UserAgent

class RequestsPage:
        
    def get_html(self, url, payload=None):
        self.url = url
        fakeuser = UserAgent()
        headers = {'user-agent': fakeuser.chrome}
        data = requests.get(url, headers=headers, params=payload)
        return data

    def save_html(self, data, filename):
        self.file = open(filename, "a")
        self.file.write(data)
        self.file.close()