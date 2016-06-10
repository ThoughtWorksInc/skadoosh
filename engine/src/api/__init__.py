import os
from urllib.parse import unquote
from uuid import uuid4
from flask import Flask, session, render_template, make_response, request, redirect, g, current_app, flash
# from flask_pymongo import PyMongo
from flask_restful import Api
# from pymongo import Connection
from bson import json_util
import json

app = Flask(__name__, instance_relative_config=False)
app.config.from_pyfile('application.cfg', silent=False)
if os.environ.get('SKADOOSH_CORE_CONFIG', None):
    app.config.from_envvar('SKADOOSH_CORE_CONFIG')

# mongo = PyMongo(app)

api = Api(app)

@api.representation('application/json')
def mjson(data, code, headers=None):
    d = json.dumps(data, default=json_util.default)
    resp = make_response(d, code)
    resp.headers.extend(headers or {})
    return resp


@app.route("/")
def home():
    name = session.get('name', "Stranger")
    return render_template('home.jinja2', name=name)

# @app.route("/recreatedb")
# def recreate_db():
#     print('Dropping database(' + app.config['MONGO_DBNAME'] + ')....\n')
#     c = Connection()
#     c.drop_database(app.config['MONGO_DBNAME'])
#     return redirect('/')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

from api.resources.help import HelpApi

api.add_resource(HelpApi, '/api/help')