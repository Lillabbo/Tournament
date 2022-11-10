from sanic import Sanic
from sanic.log import logger
from sanic.response import html, redirect


# global configuration
import config

# pages
import pages.frontpage as frontpage
import pages.Create_tournament as Create_tournament
###import pages.userprofile as profile###

app = Sanic(config.APP_NAME)
app.static('static/', 'static')
app.ctx.msg = ""


class tournement:
    def __init__(self, name, contestant, matches, description):
        self.name = name
        self.contestant = contestant
        self.matches = matches
        self.description = description

# Endpoints
@app.get("/")

async def index_page(request):
    """display frontpage"""
    
    return html(frontpage.frontpage())


@app.get("/create_tournaments")

async def tournament(request):
    """create a new tournament"""

    return html(Create_tournament.show_Tournamets())

if __name__ == '__main__':
    

    app.run(host='localhost', port=8080)
