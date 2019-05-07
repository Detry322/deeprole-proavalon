from flask_api import FlaskAPI

from debug import debug_app
from deeprole import deeprole_app

import os
import markdown

DIR = os.path.abspath(os.path.dirname(__file__))

app = FlaskAPI(__name__)

app.config['DEFAULT_RENDERERS'] = [
    'flask_api.renderers.JSONRenderer',
]

app.register_blueprint(debug_app, url_prefix='/debug')
app.register_blueprint(deeprole_app, url_prefix='/deeprole')

@app.route('/')
def index():
    with open(os.path.join(DIR, 'README.md'), 'r') as f:
        html = markdown.markdown(f.read())

    return "<!doctype HTML><html><body>{}</body></html>".format(html)

if __name__ == "__main__":
    import os
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True)
