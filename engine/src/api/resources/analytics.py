from datetime import datetime
from flask import g, request
from flask_restful import Resource, reqparse
import pymongo

from core.utils import *
from api import auth, mongo

class AnalyticsApi(Resource):
  # method_decorators = [auth.login_required]
  def __init__(self):
    self.bot_responses = mongo.db.bot_responses

  def get(self):
    data = [x for x in self.bot_responses.find(limit=100).sort([('timestamp', pymongo.DESCENDING)])]
    res = {
      'total_count': self.bot_responses.count(),
      'count': len(data),
      'data': data
    }
    return res
