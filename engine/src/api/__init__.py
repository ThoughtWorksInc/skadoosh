import os
import json
from bson import json_util
from urllib.parse import unquote
from uuid import uuid4
from flask import Flask, session, render_template, make_response, request, redirect, g, current_app, flash
from flask_restful import Api
from flask_pymongo import PyMongo
# from pymongo import Connection
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
from flask_principal import Principal, Permission, Identity, AnonymousIdentity
from flask_principal import identity_loaded, identity_changed, RoleNeed, UserNeed
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__, instance_relative_config=False)
app.config.from_pyfile('application.cfg', silent=False)
if os.environ.get('SKADOOSH_CORE_CONFIG', None):
    app.config.from_envvar('SKADOOSH_CORE_CONFIG')

mongo = PyMongo(app)
api = Api(app)
principals = Principal(app)
auth = HTTPBasicAuth()

admin_permission = Permission(RoleNeed('admin'))

users = {
  'admin@bc.com': {
    'id': 123,
    'name': "Admin",
    'password': pwd_context.encrypt("admin@123"),
    'email': 'admin@bc.com',
    'roles': ['admin']
  },
  'john@bc.com': {
    'id': 23413,
    'name': "John Smith",
    'password': pwd_context.encrypt("baby@123"),
    'email': 'john@bc.com',
    'roles': ['member']
  }
}

@auth.verify_password
def verify_password(email, password):
  print(email, password)
  if not email in users:
    user = verify_auth_token(email)
    if user:
      g.user = user
      return True
    return False
  user = users.get(email)
  if pwd_context.verify(password, user['password']):
    g.user = user
    return True
  return False

def generate_auth_token(user, expiration=600):
  s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
  return s.dumps({ 'id': user['id'], 'email': user['email'] })

def verify_auth_token(token):
  s = Serializer(app.config['SECRET_KEY'])
  try:
      data = s.loads(token)
  except SignatureExpired:
      return None # valid token, but expired
  except BadSignature:
      return None # invalid token
  user = users.get(data['email'])
  return user

@app.route('/api/token')
@auth.login_required
def get_auth_token():
  token = generate_auth_token(g.user)
  return json.dumps({ 'token': token.decode('ascii') })

@auth.error_handler
def unauthorized():
  return make_response(json.dumps({'error': 'Unauthorized access'}), 401)

@app.route('/secured')
@auth.login_required
def secured_page():
  return "This is a secured page!!"

# @auth.user_loader
# def get_user(userid):
#   if userid not in users:
#     return
#   return users.get(userid)

# @auth.request_loader
# def request_loader(request):
#    token = request.headers.get('x-auth-token', None)
#    if token is None:
#      token = request.cookies.get('x-auth-token', None)
#    if token is None or len(token) == 0 \
#     or token not in users:
#       return
#    return users.get(token)

# @auth.unauthorized_handler
# def unauthorized_handler():
#     return 'Unauthorized'

def getUserMixin(user):
  return User(user['_id'], user['name'], user['email'], user['roles'], user.get('identity', None))

class User(UserMixin):
  def __init__(self, user_id=None, name=None, email=None, roles=[], identity=None):
    self.id = user_id
    self.user_id = user_id
    self.name = name
    self.email = email
    self.roles = roles
    self.identity = identity

  def is_authenticated(self):
    return self.id is not None

  def is_anonymous(self):
    return self.id is None

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

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

from api.resources.help import HelpApi
from api.resources.analytics import AnalyticsApi

api.add_resource(HelpApi, '/api/help')
api.add_resource(AnalyticsApi, '/api/analytics')