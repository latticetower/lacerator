from bottle import route, run, template
import sys
from wfc import *

@route('/')
def index():
    return template("templates/page.tpl", name="Tanya")#'<b>Generator</b>'
    #return template('<b>Hello {{name}}</b>!', name=name)

port = 8080 if len(sys.argv)<2 else sys.argv[1]
run(host='localhost', port=port)