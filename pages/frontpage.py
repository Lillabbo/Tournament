import dominate
from dominate.tags import *

from sanic import Sanic
from config import APP_NAME

from pages.menu import show_menu






with doc:
    menu_items = [
        ('sc2 tournaments', '/'),
    ]
    show_menu(menu_items)
    with form(cls='post-form', enctype='multipart/form-data', method='POST', action='/post/image'):
        with div(cls='post'):
            input_(type='text', cls='title_inp',
                name='title',
                placeholder='Indtast titel...')
            input_(type='file', name='image', accept='image/*')
            input_(type='submit', value='Post', cls='button')
    return doc.render()
