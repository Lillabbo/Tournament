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

async def index_page(request):
    """display frontpage"""
    
    return html(frontpage.frontpage())


@app.post("/create_tournaments")

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

if __name__ == '__main__':
    

    app.run(host='localhost', port=8080)