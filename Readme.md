Voter Search
============

Voter Search is a webapp to search voters by voterid. 

Election Commission already provided a website <http://electoralsearch.in/> with uniform interface, but that is out of sync. 

The goal of this application is to provide uniform API to search for voter info of any state given voter id. Since the state election commission websites usually ask for the district, the API will have to be mirror that.

This currently supports only Karnataka.

API
---

The API has just one end point to search for an voterid. It expects two-letter state code, district number and voterid.

Example:

$ curl 'http://voter.missionvistaar.in/search?state=KA&district=1&voterid=ABC1234567'
{
	"voterid": "ABC1234567",
	"name": "Kannadiga",
	"relname": "Kannadigappa",
	"age": "36",
	"sex": "M"
	"ac": "18",
	"part": "1",
	"serial": "123",
}

Possible Use Cases
------------------

It may be useful for mapping a Voter ID to a polling booth and/or validating a Voter ID when filling a web form.
