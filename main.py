from bottle import route, run, template
import sys
from wfc import *

@route('/')
def index():
    return template("templates/page.tpl", name="Tanya")#'<b>Generator</b>'
    #return template('<b>Hello {{name}}</b>!', name=name)

if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)