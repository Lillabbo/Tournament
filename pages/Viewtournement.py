import dominate
from dominate.tags import *

from sanic import Sanic
from config import APP_NAME


from pages.menu import show_menu
import pages.selfmade_classes as tournaments
from pages.Create_tournament import all_tournaments


def top_bar():
    doc = dominate.document(title="SC2 Tournaments")
    with doc.head:
        pass
    with doc:
        menu_items = [
            ('sc2 tournaments', '/'),
            ('create tournament','/create_tournaments'),
            ('view tournaments','/view_tournaments')
        ]
        show_menu(menu_items)
            
        p1= tournaments.tournament("T1","8","7","fake(r) tournament")
        p1.show_tournaments()
    return doc.render()


