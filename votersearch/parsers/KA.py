from .base import BaseParser
import logging

logger = logging.getLogger(__name__)

class Parser(BaseParser):
    URL = "http://ceokarnataka.kar.nic.in/SearchWithEpicNo_New.aspx"    

    def get_voter_details(self, state, district, voterid):
        self.get(self.URL)
        formdata = self.get_formdata()

        formdata['ctl00$ContentPlaceHolder1$ddlDistrict'] = str(district)
        formdata['ctl00$ContentPlaceHolder1$txtEpic'] = voterid
        formdata['ctl00$ContentPlaceHolder1$btnSearch'] = 'Search'

        self.post(self.URL, formdata)
        soup = self.get_soup()

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
