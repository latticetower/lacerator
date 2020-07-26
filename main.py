from bottle import route, run, template
import os
from wfc import *

@route('/pattern-generator/<h>/<w>')
def generate_wfc(h, w):
    return template("templates/pattern-generator.html",
        svg=make_pattern_from_fragments(h, w))#'<b>Generator</b>'
    #return template('<b>Hello {{name}}</b>!', name=name)


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