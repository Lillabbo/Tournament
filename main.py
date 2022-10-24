from sanic import Sanic
from sanic.log import logger
from sanic.response import html, redirect


# global configuration
import config

# pages
import pages.frontpage as frontpage
###import pages.userprofile as profile###

app = Sanic(config.APP_NAME)
app.static('static/', 'static')
app.ctx.msg = ""

# Endpoints
@app.get("/")
@protected
async def index_page(request):
    """Display all posts."""
    
    return html(frontpage.show_posts(all_posts))


@app.post("/create_tournaments")
@protected
async def tournament(request):
    """create a new tournament"""
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

    fname = f'static/images/posts/{img_id}.{imgtype}'
    with open(fname, 'wb') as f:
        f.write(img.body)

    return redirect("/")



app.run(host='localhost', port=8080)