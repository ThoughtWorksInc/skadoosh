from datetime import datetime
from flask import g, request
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('text',required=False,type=str)

class HelpApi(Resource):
  def post(self):
    args = parser.parse_args()
    input_text = args['text']
    if input_text is None or len(input_text) == 0:
        input_text = "nothing!! What's up? Are you okay?"
    return "You said '%s'" % (input_text)
