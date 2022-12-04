import dominate
from dominate.tags import *

from sanic import Sanic
from config import APP_NAME

import pages.selfmade_classes as tournaments
from pages.menu import show_menu
all_tournaments={}


def Create_Tournaments():
    app = Sanic.get_app(APP_NAME)
    doc = dominate.document(title=f'{APP_NAME} | Create_Tournamets')
   
    with doc.head:
        menu_items = [
            ('sc2 tournaments', '/'),
            ('sc2 Create tournaments', '/'),
            ('view tournaments','/view_tournaments')
        ]
        show_menu(menu_items)
        link(rel='stylesheet', href=app.url_for('static', name="static", filename="style.css"))
    with doc:
        h1("Create Tournaments", cls='page_header')
        with div(cls='SC2 Create Tournaments'):

            with form(method="POST", action="/newtournament"):
                tname=str(input_(type = "text", cls = "textinput", placeholder="type in tournament name...", name="name"))
                tpart=str(input_(type = "text", cls = "textinput", placeholder="type in number of participants...", name="nparti"))
                tdesc=str(input_(type="text", cls="textinput", placeholder="description...", name="desc"))
                input_(type="submit", value="Opret turnering", cls="button")
                all_tournaments.update({tname:tournaments.tournament(tname,tpart,"0",tdesc)})
    return doc.render()

