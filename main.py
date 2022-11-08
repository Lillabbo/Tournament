from sanic import Sanic
from sanic.log import logger
from sanic.response import html, redirect


# global configuration
import config

# pages
import pages.frontpage as frontpage
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

class matches:
    def __init__(self, contestant_A,contestant_B, ):
        self.contestant_A = contestant_A
        self.contestant_B = contestant_B

# Endpoints
@app.get("/")

async def index_page(request):
    """display frontpage"""
    
    return html(frontpage.frontpage())


@app.post("/create_tournaments")

async def tournament(request):
    """create a new tournament"""

    return redirect("/")

if __name__ == '__main__':
    

    app.run(host='localhost', port=8080)
