import dominate
from dominate.tags import *

from sanic import Sanic
from config import APP_NAME


from pages.menu import show_menu





def frontpage():
    doc = dominate.document(title="SC2 Tournaments")
    with doc:
        menu_items = [
            ('sc2 tournaments', '/'),
        ]
        show_menu(menu_items)
        
                
    return doc.render()
