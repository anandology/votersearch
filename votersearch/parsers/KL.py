from .base import BaseParser
import logging

logger = logging.getLogger(__name__)

class Parser(BaseParser):
    BASE_URL = "http://www.ceo.kerala.gov.in/rollsearch.html"
    URL = "http://www.ceo.kerala.gov.in/electoralroll/edetailListAjax.html?lacNo=1&distNo={district}&epicNo={voterid}"    

    def get_voter_details(self, state, district, voterid):
        url = self.URL.format(district=district, voterid=voterid)

        # first time it fails with internal error
        # we need to try this two to get the right cookie
        self.get(self.BASE_URL)
        self.get(self.BASE_URL)

        d = self.get(url).json()
        if d.get('ERROR') or d.get('iTotalRecords') != 1:
            return

        name, relname, house, serial, ac, part = d['aaData'][0][:6]

        # provide only required fields to avoid breaking API later
        d2 = {
            'voterid': voterid,
            'name': name,
            'relname': relname,
            'sex': '-',
            'age': 0,
            'ac': ac,
            'part': part,
            'serial': serial,
        }
        logger.info("voter info %s %s", voterid, d2)    
        return d2
