import dominate
from dominate.tags import *

from sanic import Sanic
from config import APP_NAME


from pages.menu import show_menu

def Create_Tournamets():
    doc = dominate.document(title="SC2 Create Tournaments")
    with doc.head:
        menu_items = [
            ('sc2 tournaments', '/'),
            ('sc2 Create tournaments', '/'),
        ]
        show_menu(menu_items)
                       
    return doc.render()