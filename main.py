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

# DAOs
import database.user as user
import database.post as post

# auth
from auth import protected, new_token, del_token

# pages
import pages.posts as posts
import pages.userprofile as profile

app = Sanic(config.APP_NAME)
app.static('static/', 'static')
app.ctx.msg = ""

# Create image folders
pathlib.Path("static/images/icons").mkdir(parents=True, exist_ok=True)
pathlib.Path("static/images/posts").mkdir(parents=True, exist_ok=True)

# Create database tables
userDAO = user.UserDAO()
postDAO = post.PostDAO()
userDAO.create_table()
postDAO.create_table()

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

@app.get("/logout")
@protected
async def logout(request):
    """Log the user out."""
    del_token(request.ctx.username)
    logger.info(f"Logged out: {request.ctx.username}")
    return redirect("/")

@app.post("/update_profile")
@protected
async def update_profile(request):
    """Receive and save updated profile information."""
    user = userDAO.get_user(request.ctx.username)
    print(request.form)
    print(request.files)

    if('profile-icon' in request.files and
       request.files['profile-icon'] and
       request.files['profile-icon'][0].body):
        old_filename = user.img_path
        iconfile = request.files['profile-icon'][0]
        imgtype = iconfile.type[6:]
        img_id = str(uuid.uuid4())
        img_path = f'images/icons/{img_id}.{imgtype}'
        fname = f'static/{img_path}'
        with open(fname, 'wb') as f:
            f.write(iconfile.body)
        if old_filename is not None:
            os.remove(f'static/{old_filename}')
        user.img_path = img_path

    if('description' in request.form and request.form['description']):
        desc = request.form['description'][0]
        user.desc = desc

    userDAO.update(user)
    return redirect("/profile")

@app.post("/post/text")
@protected
async def make_post(request):
    """Receive and store new text post."""
    if not ('title' in request.form and
            request.form['title']):
        return redirect("/write")
    
    title = request.form['title'][0]
    contents = ""
    if 'contents' in request.form and request.form['contents']:
        contents = request.form['contents'][0]

    usrid = userDAO.get_user_id(request.ctx.username)

    pst = post.TextPost(usrid, title, datetime.datetime.utcnow(), contents)
    postDAO.store(pst)
    return redirect("/")

@app.post("/post/image")
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

@app.post("/login")
async def login(request):
    """Log user in, then redirect to front page."""
    if not ('uname' in request.form and
            'pword' in request.form and
            request.form['uname']   and
            request.form['pword']):
        app.ctx.msg = "Udfyld alle felter."
        return redirect("/")

    username = request.form['uname'][0]
    password = request.form['pword'][0]

    usr = userDAO.get_user(username)
    if not usr:
        app.ctx.msg = "Brugernavn findes ikke."
        return redirect("/")

    k = usr.make_key(password)
    if k != usr.key:
        app.ctx.msg = "Forkert adgangskode."
        return redirect("/")

    tok = new_token(username)
    resp = redirect("/")
    resp.cookies['auth'] = username + ':' + tok
    resp.cookies['auth']['expires'] = datetime.datetime.utcnow() +\
                                      datetime.timedelta(days=1)
    return resp

@app.post("/register")
async def register(request):
    """Create a new user, then log them in."""
    if not ('uname'  in request.form and
            'pword'  in request.form and
            'rpword' in request.form and
            request.form['uname']    and
            request.form['pword']    and
            request.form['rpword']):
        app.ctx.msg = "Udfyld alle felter."
        return redirect("/")
    
    username = request.form['uname'][0]
    password1 = request.form['pword'][0]
    password2 = request.form['rpword'][0]

    if password1 != password2:
        app.ctx.msg = "Passwords matcher ikke."
        return redirect("/")

    try:
        usr = userDAO.new(username, password1)
        userDAO.store(usr)
        logger.info(f"New user: {username}")
        return await login(request)
    except user.UserExistsError as err:
        logger.info(str(err))
        app.ctx.msg = f"Brugernavnet {username} er optaget."
        return redirect("/")

app.run(host='localhost', port=8080)