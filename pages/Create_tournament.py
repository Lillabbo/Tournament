import dominate
from dominate.tags import *

from sanic import Sanic
from config import APP_NAME


from pages.menu import show_menu

def SC2_Create_Tournamets():
    doc = dominate.document(title="SC2 Create Tournaments")
    with doc.head:
        menu_items = [
            ('sc2 tournaments', '/'),
            ('sc2 Create tournaments', '/'),
        ]
        show_menu(menu_items)
            
    return doc.render()

Player = {'victories':}

#Indsæt spillerens navn til en dictionary med key
def enter_names():
    n= form(method="recall_name")
    input_(type="text")
         #("enter name")
    d={}
    for i in range (n):
         key=input("enter spiller: ")
         value= input("enter name")
         d[key]=value
    print(d)

# # Opret spillere knap og indsæt navn
# def add_contestant():
#     with ul(cls='Add_contestant'):
#         for (txt, lnk) in add_contestant:
#             with div(cls='Add_contestant'):
#                     a(txt, cls='button', href=lnk)    
#     with form()

# 
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
                input_(type = "text", cls = "textinput", placeholder="type in tournament name...", name="name")
                input_(type = "number of participants", cls = "textinput", placeholder="type in number of participants...", name="name")
                input_(type="description", cls="textinput", placeholder="description...")
                input_(type="submit", value="Opret turnering", cls="button")
    return doc.render()

