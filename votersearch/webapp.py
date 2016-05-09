import sys
import web
import json
from . import parsers

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
        if headers:
            web.header("Access-Control-Allow-Headers", headers)
        return ""

    def GET(self):
        self.OPTIONS()
        i = web.input(state="KA", district="21")
        voterid = i.get("voterid")
        data = parsers.get_voter_details(i.state, i.district, voterid)
        web.header("content-type", "application/json")
        return json.dumps(data)

def main():
    if "--search" in sys.argv:
        sys.argv.remove("--search")
        state, district, voterid = sys.argv[1:]
        print parsers.get_voter_details(state, district, voterid)
    else:
        app.run()

if __name__ == '__main__':
    main()