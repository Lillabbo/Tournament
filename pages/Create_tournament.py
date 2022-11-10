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
    with
        show_menu(menu_items)
                       
    return doc.render()

def show_Tournamets():
    with ul(cls='Create_Tournamets'):
        for (txt, lnk) in Create_Tournamets:
            with div(cls='Create_Tournamets'):
                    a(txt, cls='button', href=lnk)


def add_contestant():
    import main class tournement