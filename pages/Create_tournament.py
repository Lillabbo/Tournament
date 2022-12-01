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

def show_Tournamets():
    with ul(cls='Create_Tournamets'):
        for (txt, lnk) in SC2_Create_Tournamets:
            with div(cls='Create_Tournamets'):
                    a(txt, cls='button', href=lnk)

def enter_values():
    n= int(input("enter elemets"))
    d={}
    for i in range (n):
        key=input("enter KEY: ")
        value= input("enter value")
        d[key]=value
    print(d)

def add_contestant():
     with ul(cls='Add_contestant'):
        for (txt, lnk) in add_contestant:
            with div(cls='Add_contestant'):
                    a(txt, cls='button', href=lnk)    
     with form(enter_values):
    
        return()

def Create_Tournaments():
    app = Sanic.get_app(APP_NAME)
    doc = dominate.document(title=f'{APP_NAME} | Create_Tournamets')

    with doc.head:
        link(rel='stylesheet', href=app.url_for(
            
        ))
    with doc:
        h1("Create_Tournamets", cls='page_header')
        with div(cls=button):
            return()