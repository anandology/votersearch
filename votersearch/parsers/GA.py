from .base import BaseParser
import logging

logger = logging.getLogger(__name__)

class Parser(BaseParser):
    URL = "http://ceogoa.nic.in/appln/UIL/ElectoralRollSearch.aspx"

    def get_voter_details(self, state, district, voterid):
        self.get(self.URL)
        formdata = self.get_formdata()

        formdata['ctl00$Main$drpDistrict'] = str(district)
        formdata['ctl00$Main$txtEpic'] = voterid
        formdata['ctl00$Main$rdlCriteria'] = 'EPIC'
        formdata['ctl00$Main$rdlSearchType'] = 'DISTRICT'
        formdata['ctl00$Main$btnSearch'] = 'Search'
        formdata['ctl00$ToolkitScriptManager'] = 'ctl00$ToolkitScriptManager|ctl00$Main$btnSearch'
        formdata['__ASYNCPOST'] = True


        self.post(self.URL, formdata)
        soup = self.get_soup()
        table = soup.find("table", {"id": "ctl00_Main_gvElector"})
        if not table:
            return None
        last_row = table.findAll("tr")[-1]
        data = [td.getText().strip() for td in last_row.findAll(("td", "tr"))]
        cols = "ac_num part_no section_no sl_no h_no name name_vernacular rel_name rel_name_vernacular sex".split()
        d = dict(zip(cols, data))
        d['voterid'] = voterid

        # provide only required fields to avoid breaking API later
        d2 = {
            'voterid': voterid,
            'name': d['name'].encode('ascii', 'ignore'),
            'relname': d['rel_name'].encode('ascii', 'ignore'),
            'sex': d['sex'],
            'age': d.get('age'),
            'ac': d['ac_num'],
            'part': d['part_no'],
            'serial': d['sl_no'],
        }
        logger.info("voter info %s %s", voterid, d2)
        return d2
