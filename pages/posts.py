from urllib.parse import quote
import dominate
from dominate.tags import *

from sanic import Sanic
from config import APP_NAME

import pages.userprofile as userprofile
from pages.menu import show_menu
import database.post as post

def show_posts(posts=[], user=None):
    app = Sanic.get_app(APP_NAME)
    doc = dominate.document(title=f'{APP_NAME} | Posts')

    with doc.head:
        link(rel='stylesheet', href=app.url_for('static',
                                                name='static',
                                                filename='style.css'))

    with doc:
        menu_items = [
            ('Forside', '/'),
            ('Log ud', '/logout'),
            ('Ny post', '/write'),
            ('Nyt billede', '/upload'),
            ('Rediger profil', '/profile')
        ]
        show_menu(menu_items)
        if user is not None:
            userprofile.user_profile(user)
        for display_post in posts:
            with div(cls='post'):
                h1(display_post.post.title)
                with div(cls='author'):
                    a(f'af: {display_post.author.username}',
                        href=f'/u/{quote(display_post.author.username)}',
                        cls='author_link')
                if isinstance(display_post.post, post.TextPost): # text post
                    with div():
                        lines = filter(bool, display_post.post.contents.splitlines())
                        for par in lines:
                            p(par)
                else: # image post
                    with div():
                        img(src=app.url_for('static',
                                            name='static',
                                            filename=f'images/posts/{display_post.post.image_path}'))

    return doc.render()

def create_image_page():
    app = Sanic.get_app(APP_NAME)
    doc = dominate.document(title=f'{APP_NAME} | Upload billede')

    with doc.head:
        link(rel='stylesheet', href=app.url_for('static',
                                                name='static',
                                                filename='style.css'))

    with doc:
        menu_items = [
            ('Forside', '/'),
            ('Log ud', '/logout'),
            ('Ny post', '/write'),
            ('Rediger profil', '/profile')
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
            ('Log ud', '/logout'),
            ('Nyt billede', '/upload'),
            ('Rediger profil', '/profile')
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