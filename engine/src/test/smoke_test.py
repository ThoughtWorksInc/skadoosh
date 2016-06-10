import unittest
import requests

url = 'http://localhost:4000/api/help'

class SmokeTestHelpApi(unittest.TestCase):

    def test_samplequestion(self):
        response = requests.post(url,data=dict(text='Hello'))
        self.assertEqual(response.text, '"You said \'Hello\'"')

    def test_isupper(self):
        response = requests.post(url,data=dict(text=None))
        self.assertEqual(response.text, '"You said \'nothing!! What\'s up? Are you okay?\'"')