import dominate
from dominate.tags import *

from sanic import Sanic
from config import APP_NAME


from pages.menu import show_menu





def frontpage():
    doc = dominate.document(title="SC2 Tournaments")
    with doc.head:
        menu_items = [
            ('sc2 tournaments', '/'),
            ('create tournament','/create_tournaments'),
            ('view tournaments','/view_tournaments')
        ]
        show_menu(menu_items)
        
                
    return doc.render()
