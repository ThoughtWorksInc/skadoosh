from datetime import datetime
from flask import g, request
from flask_restful import Resource, reqparse
from api import auth, mongo

from core.glados import Glados
from core.utils import *

help_agent = Glados()

test_account_info = {
  'name': 'Nikes',
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
  def __init__(self):
    self.bot_responses = mongo.db.bot_responses
  # method_decorators = [auth.login_required]
  def post(self):
    args = parser.parse_args()
    input_text = args['text']
    if isEmpty(input_text):
      return "You said nothing!! What's up? Are you okay?"
    ans = help_agent.get_help(input_text)
    answer = ans['answer']
    if isEmpty(answer):
      return "Sorry! I don't understand what you said. Can you ask other topics?"
    ans['answer'] = self.apply_context(ans['answer'])
    ans['timestamp'] = get_timestamp()
    self.save(ans)
    return ans
    
  def save(self, orginal):
    response = orginal.copy()
    response['user_id'] = 0
    if 'user' in g and g.user is not None:
      response['user_id'] = g.user['id'] 
    self.bot_responses.save(response)
   
  def apply_context(self, text):
      return text % test_account_info 
    
