import web
import json
from . import voterlib

urls = (
    "/search", "search"
)
app = web.application(urls, globals())
application = app.wsgifunc()

class search:
    def OPTIONS(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header("Access-Control-Allow-Methods", "GET")
        headers = web.ctx.env.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS')
        print web.ctx.env
        if headers:
            web.header("Access-Control-Allow-Headers", headers)
        return ""

    def GET(self):
        self.OPTIONS()
        i = web.input()
        voterid = i.get("voterid")
        data = voterlib.get_voter_details(voterid)
        web.header("content-type", "application/json")
        return json.dumps(data)

if __name__ == '__main__':
    app.run()
