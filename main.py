from bottle import route, template, redirect, static_file, error, run
import os

from utils import *

@route('/about')
def show_home():
    return template('about')

@route("/pattern-generator")
@route('/pattern-generator/<h>/<w>')
def generate_wfc(h=10, w=10):
    return template("templates/pattern-generator.html",
        filename=make_pattern_from_fragments(h, w))#'<b>Generator</b>'
    #return template('<b>Hello {{name}}</b>!', name=name)

@route('/css/<filename>')
def send_css(filename):
    return static_file(filename, root='static/css')

@route('/assets/<filename>')
def send_asset(filename):
    return static_file(filename, root='static/svg')
# TODO: check type

@error(404)
def error404(error):
    return template('error', error_msg='404 error. Nothing to see here')


@route('/simple-generator')
def generate_wfc():
    return template("templates/pattern-generator.html",
        svg=make_pattern_measured(3))#'<b>Generator</b>'
    #return template('<b>Hello {{name}}</b>!', name=name)


@route('/')
def index():
    return template("templates/page.tpl", name=".")#'<b>Generator</b>'
    #return template('<b>Hello {{name}}</b>!', name=name)

if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)