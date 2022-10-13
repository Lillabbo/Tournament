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
    all_posts = postDAO.fetch_all_display()
    return html(posts.show_posts(all_posts))

@app.get("/u/<username>")
@protected
async def user_page(request, username: str):
    """Display all posts from the given user."""
    user = userDAO.get_user(username)
    all_posts = postDAO.fetch_by_user(unquote(username))
    return html(posts.show_posts(all_posts, user=user))

@app.get("/write")
@protected
async def write_page(request):
    """Let user write a new text post."""
    return html(posts.create_page())

@app.get("/upload")
@protected
async def write_page(request):
    """Let user create a new image post."""
    return html(posts.create_image_page())

@app.get("/profile")
@protected
async def edit_profile(request):
    """Let user see and edit their own profile page."""
    user = userDAO.get_user(request.ctx.username)
    return html(profile.edit_profile(user))




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