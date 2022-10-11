from functools import wraps
from sanic.response import html

from base64 import b64encode
import os

from pages.login import login_page

tokens = {}

def new_token(username):
    tok = b64encode(os.urandom(32)).decode('utf-8')
    tokens[username] = tok
    return tok

def del_token(username):
    del tokens[username]

def check_token(request):
    if not 'auth' in request.cookies:
        return False
    ls = request.cookies['auth'].split(':')
    if len(ls) != 2:
        return False
    [username, tok] = ls
    request.ctx.username = username
    return username in tokens and tokens[username] == tok


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)

            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return html(login_page(), 401)

        return decorated_function

    return decorator(wrapped)