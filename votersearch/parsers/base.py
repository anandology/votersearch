import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)
class BaseParser(object):
    def __init__(self):
        self.response = None
        self.session = requests.session()        

    def get(self, url):
        logger.info("GET %s", url)
        self.response = self.session.get(url)
        return self.response
        
    def post(self, url, data):
        logger.info("POST %s", url)
        self.response = self.session.post(url, data)
        return self.response

    def get_soup(self):
        """Returns BeautifulSoup object for the response from the last get/post call.
        """
        return BeautifulSoup(self.response.text, "lxml")

    def get_formdata(self):
        soup = self.get_soup()
        inputs = soup.find_all("input", attrs={"type": "hidden"})
        formdata = {f['name']: f['value'] for f in inputs}

        formdata['__EVENTTARGET'] = ''
        formdata['__EVENTARGUMENT'] = ''
        formdata['__LASTFOCUS'] = ''

        return formdata