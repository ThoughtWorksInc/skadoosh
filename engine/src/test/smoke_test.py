import unittest
import requests

url = 'http://localhost:4000/api/help'

class SmokeTestHelpApi(unittest.TestCase):

    def test_sampleQuestion(self):
        response = requests.post(url,data=dict(text='Tell the account balance.'))
        self.assertEqual(response.json(), 'Your account balance is 323710.38')

    def test_emptyInput(self):
        response = requests.post(url,data=dict(text=None))
        self.assertEqual(response.json(), "You said nothing!! What\'s up? Are you okay?")