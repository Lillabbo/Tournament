from urllib.parse import unquote
from sanic import Sanic
from sanic.log import logger
from sanic.response import html, redirect

import uuid
import datetime
import os
import pathlib

# global configuration
import config

# pages
import pages.posts as posts
import pages.userprofile as profile

app = Sanic(config.APP_NAME)
app.static('static/', 'static')
app.ctx.msg = ""

# Create image folders
pathlib.Path("static/").mkdir(parents=True, exist_ok=True)
pathlib.Path("static/").mkdir(parents=True, exist_ok=True)


# Endpoints
@app.get("/")
@protected
async def index_page(request):
    """Display all posts."""
    
    return html(posts.show_posts(all_posts))


@app.post("/create_tournaments")
@protected
async def make_img_post(request):
    """Receive and store new image post."""
    if not ('title' in request.form and
            request.form['title']):
        print("MISSING TITLE")
        return redirect("/upload")

    if not ('image' in request.files and
            request.files['image'] and
            request.files['image'][0].body):
        return redirect("/upload")
    
    title = request.form['title'][0]
    img = request.files['image'][0]
    imgtype = img.type[6:]

    usrid = userDAO.get_user_id(request.ctx.username)

    img_id = str(uuid.uuid4())
    pst = post.ImagePost(usrid, title, datetime.datetime.utcnow(), f'{img_id}.{imgtype}')
    postDAO.store(pst)

    fname = f'static/images/posts/{img_id}.{imgtype}'
    with open(fname, 'wb') as f:
        f.write(img.body)

    return redirect("/")



app.run(host='localhost', port=8080)