from datetime import datetime
from flask import g, request
from flask_restful import Resource, reqparse
from api import auth

from core.glados import Glados
from core.utils import *

help_agent = Glados()

test_account_info = {
  'name': 'John',
  'balance': 323710.38,
  'account_no': 12900989124,
  'phone': 73710203,
  'reward_points':525,
  'reward_points_expiring':200,
  'reward_points_expiring_on': '15-09-2016'
}
  
parser = reqparse.RequestParser()
parser.add_argument('text',required=False,type=str)

class HelpApi(Resource):
  # method_decorators = [auth.login_required]
  def post(self):
    args = parser.parse_args()
    input_text = args['text']
    if isEmpty(input_text):
      return "You said nothing!! What's up? Are you okay?"
    ans = help_agent.get_help(input_text)
    if isEmpty(ans):
      return "Sorry! I don't understand what you said. Can you ask other topics?"
    return ans % test_account_info
