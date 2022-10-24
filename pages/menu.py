from dominate.tags import *

def show_menu(menu_items):
    with ul(cls='menu'):
        for (txt, lnk) in menu_items:
            with li(cls='menu-item'):
                a(txt, cls='button', href=lnk)