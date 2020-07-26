from bottle import route, run, template

from wfc import *

@route('/')
def index():
    return template("templates/page.tpl", name="Tanya")#'<b>Generator</b>'
    #return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=80)