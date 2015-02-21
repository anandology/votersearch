"""module to load voter details from EC website.

Currently only works for Bangalore.
"""
import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

URL = "http://ceokarnataka.kar.nic.in/SearchWithEpicNo_New.aspx"

def get_voter_details(voterid):
    s = requests.session()
    r = s.get(URL)
    soup = BeautifulSoup(r.text, "lxml")
    inputs = soup.find_all("input", attrs={"type": "hidden"})
    formdata = {f['name']: f['value'] for f in inputs}

    formdata['__EVENTTARGET'] = ''
    formdata['__EVENTARGUMENT'] = ''
    formdata['__LASTFOCUS'] = ''

    formdata['ctl00$ContentPlaceHolder1$ddlDistrict'] = '21'
    formdata['ctl00$ContentPlaceHolder1$txtEpic'] = voterid
    formdata['ctl00$ContentPlaceHolder1$btnSearch'] = 'Search'

    r = s.post(URL, formdata)

    soup = BeautifulSoup(r.text)
    table = soup.find("table", {"id": "ctl00_ContentPlaceHolder1_GridView1"})
    if not table:
        return None
    last_row = table.findAll("tr")[-1]
    data = [td.getText() for td in last_row.findAll(("td", "tr"))]
    # skip the first one, which is a button
    data = data[1:]
    cols = "ac_num ac_name part_no sl_no first_name last_name rel_firstname rel_lastname sex age".split()
    d = dict(zip(cols, data))
    d['voterid'] = voterid

    def join(a, b):
        c = a + u" " + b
        return c.encode('ascii', 'ignore').strip()

    # provide only required fields to avoid breaking API later
    d2 = {
        'voterid': voterid,
        'name': join(d['first_name'], d['last_name']),
        'relname': join(d['rel_firstname'], d['rel_lastname']),
        'sex': d['sex'],
        'age': d['age'],
        'ac': d['ac_num'],
        'part': d['part_no'],
        'serial': d['sl_no'],
    }
    logger.info("voter info %s %s", voterid, d2)    
    return d2

if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.INFO, format = "[%(levelname)s] : %(filename)s:%(lineno)d : %(message)s")
    print get_voter_details(sys.argv[1])
