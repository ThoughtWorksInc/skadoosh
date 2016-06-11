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


    def test_rewards_points(self):
        response = requests.post(url,data=dict(text='How many points do I have?'))
        self.assertEqual(response.json(), "You have 525 points.")

    def test_rewards_points_variation(self):
        response = requests.post(url,data=dict(text='How many reward points do I have?'))
        self.assertEqual(response.json(), "You have 525 points.")


    def test_rewards_expire(self):
        response = requests.post(url,data=dict(text='When do my points expire?'))
        self.assertEqual(response.json(), "Your 200 points expire on 15th September.")