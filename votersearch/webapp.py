import web
import json
from . import voterlib

urls = (
    "/search", "search"
)
app = web.application(urls, globals())

class search:
    def GET(self):
        i = web.input()
        voterid = i.get("voterid")
        data = voterlib.get_voter_details(voterid)
        web.header("content-type", "application/json")
        return json.dumps(data)

if __name__ == '__main__':
    app.run()