Voter Search
============

Voter Search is a webapp to search voters by voterid. 

Election Commission already provided a website <http://electoralsearch.in/> with uniform interface, but that is out of sync. 

The goal of this application is to provide uniform API to search for voter info of any state given voter id. Since the state election commission websites usually ask for the district, the API will have to be mirror that.

Proposed API
------------

* `/search?state=KA&district=12&voterid=ABC1234567`

Searches for voter in given state and district.

* `/search?state=KA&ac=135&voterid=ABC1234567`

Searches for voter in given assembly constituency.

Web Interface
-------------

It may be useful to provide a web interface to search by voterid by filling a form.

Implementation
--------------

For implementing this we'll have to write one parser for each state. The implementation may cache the results temporarily for some time, should not be stored permanantly. 

