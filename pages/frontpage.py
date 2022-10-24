import dominate
from dominate.tags import *

from sanic import Sanic
from config import APP_NAME








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

def create_page():
    app = Sanic.get_app(APP_NAME)
    doc = dominate.document(title=f'{APP_NAME} | Skriv')

    with doc.head:
        link(rel='stylesheet', href=app.url_for('static',
                                                name='static',
                                                filename='style.css'))

    with doc:
        menu_items = [
            ('Forside', '/'),
        ]
        show_menu(menu_items)
        with form(cls='post-form', method='POST', action='/post/text'):
            with div(cls='post'):
                input_(type='text', cls='title_inp',
                        name='title',
                        placeholder='Indtast titel...')
                textarea(cls='contents_inp',
                            name='contents',
                            placeholder='Indtast tekst...')
            input_(type='submit', value='Post', cls='button')

    return doc.render()