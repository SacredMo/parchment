#-*- coding:utf-8 -*-
from flask import render_template,  request,session ,Flask, current_app
from flask_principal import Principal, Permission, UserNeed, RoleNeed, Identity, AnonymousIdentity, identity_changed, identity_loaded
from datetime import datetime
from core import models
import simplejson as json

from logging import Formatter
import logging.handlers,logging

LOG_FILENAME = 'logs/blog.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=100000000, backupCount=5)
handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(process)d - Line:%(lineno)d - %(message)s'))

app = Flask("parchment",static_folder='static', template_folder='templates')
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?R1'

# load the extension
principals = Principal(app)

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))

@app.errorhandler(401)
def unauthorized(e):
    return render_template('errors.html',message ="unauthorized" ), 401

@app.errorhandler(400)
def page_not_found(e):
    return render_template('errors.html', message=e.description), 400

@app.errorhandler(403)
def access_forbidden(e):
    return render_template('errors.html', message=e.description), 403

@app.errorhandler(404)
def access_notfound(e):
    return render_template('errors.html', message='The requested URL was not found on the server. '), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('index.html'), 500

@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    if 'index' in request.path :
        return index()
    app.logger.info("request path:  %s" %(request.path))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def login():
    args = {"category":"","tags":[]}
    return render_template('add.html',args=args)

@app.route('/atg/<name>', methods=['GET', 'POST'])
def add_tag():
    tag = models.BlogTag(name)
    tm = models.TagManager()
    tm.add(tag)
    return "ok"

@app.route('/rmtg/<id>', methods=['GET', 'POST'])
def remove_tag():
    tm = models.TagManager()
    tm.remove(id)
    return "ok"

@app.route('/acategory/<name>', methods=['GET', 'POST'])
def add_category():
    ctgr = models.BlogCategory(name)
    cm = models.CategoryManager()
    cm.add(ctgr)
    return "ok"

@app.route('/rmcategory/<id>', methods=['GET', 'POST'])
def remove_category():
    cm = models.CategoryManager()
    cm.remove(id)
    return "ok"

@app.route('/ablog', methods=['GET', 'POST'])
def add_blog():
    title = request.form.get('title',"")
    tags = request.form.get('tags').split(',')
    category = request.form.get('category',"")
    content = request.form.get('content',"")
    public = request.form.get('public',0)

    app.logger.debug("**************************")
    app.logger.debug("title:%s"%title)
    app.logger.debug("tags:%s"%tags)
    app.logger.debug("content:%s"%content)
    app.logger.debug("**************************")
    blog = models.Blog(title,tags,category,content,public)
    bm = models.BlogManager()
    bm.add(blog)
    return render_template('index.html')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)