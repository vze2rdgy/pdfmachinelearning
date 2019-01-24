import os
import logging
from flask import Flask
from flask import render_template, redirect, url_for, send_from_directory
from core.data import api
from datetime import datetime
import WebConsts


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app(testconfig = None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        )
    if testconfig is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in.
        app.config.from_mapping(testconfig)
    #ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    api.setup_db_session(app)

    from flask_bp_search import search_bp
    app.register_blueprint(search_bp)

    from flask_bp_suppliers import supplier_bp
    app.register_blueprint(supplier_bp)

    from webapi.flask_bp_webapi import webapi_bp
    app.register_blueprint(webapi_bp)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    #@app.route('/<path:path>')
    #def send_js(path):
    #    return send_from_directory('static/ng', path)

    #@app.route("/", methods=['GET', 'POST'])
    #def home():
    #    return render_template(
    #        'index.html',
    #        title='Home Page' 
    #    )

    @app.route("/")
    def searchhome():
        return redirect(url_for("search.home"))
    
    @app.route("/supplier")
    def supplierhome():
        return redirect(url_for("supplier.home"))
    #@app.route("/hello")
    #def hello():
    #    print(app.app_context().g)
    #    return "Hello, World!"

    return app

def startapp():
    return create_app({
        "DEBUG": True,
        "ENV" : "production"
        })

if __name__ == "__main__":
    print("running iclap web app")
    startapp().run()

