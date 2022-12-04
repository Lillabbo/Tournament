from sanic import Sanic
from sanic.log import logger
from sanic.response import html, redirect


# global configuration
import config

# pages
import pages.frontpage as frontpage
import pages.Viewtournement as show_tournament
import pages.Create_tournament as Create_tournament
###import pages.userprofile as profile###
import pages.selfmade_classes as all_classes
app = Sanic(config.APP_NAME)
app.static('static/', 'static')
app.ctx.msg = ""





# Endpoints
@app.get("/")

async def index_page(request):
    """display frontpage"""
    
    return html(frontpage.frontpage())


@app.get("/create_tournaments")

async def tournament(request):
    """create a new tournament"""

    return html(Create_tournament.Create_Tournaments())



@app.get("/view_tournaments")

async def show_tournaments(request):
    """display frontpage"""
    
    return html(show_tournament.top_bar())

@app.post("/newtournament")
async def new_tournament(request):
    name = request.form.get("name")
    print(name)
    return redirect("/")


if __name__ == '__main__':
    

    app.run(host='localhost', port=8080)    