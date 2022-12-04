import dominate
from dominate.tags import *

from sanic import Sanic
from config import APP_NAME

import pages.selfmade_classes as tournaments
from pages.menu import show_menu
from pages.Create_tournament import all_tournaments
participant_names=[]
def editor():
    doc = dominate.document(title="SC2 Tournaments")
    with doc.head:
        menu_items = [
            ('sc2 tournaments', '/'),
            ('create tournament','/create_tournaments'),
            ('view tournaments','/view_tournaments')
        ]
        show_menu(menu_items)
    with doc:
        with div(cls='SC2 Create Tournaments'):

            with form(method="POST", action="/newtournament"):
                tname=str(input_(type = "text", cls = "textinput", placeholder="type in tournament name...", name="name"))
                tpart=str(input_(type = "text", cls = "textinput", placeholder="type in the name of a participant", name="participant"))
                input_(type="submit", value="Opdater turnering", cls="button")
                participant_names.append(tpart)
                all_tournaments.update({tname:participant_names})

                
    return doc.render()
