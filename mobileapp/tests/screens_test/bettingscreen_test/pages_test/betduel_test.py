"""
File testing the right behavior of betpage.py
"""
from unittest.mock import patch

from kivy.lang.builder import Builder

from screens.bet.pages.betduel.betduel_page import *

Builder.load_file(None)

class TestBetDuelPage:
	object_to_test = None
	bet = Bet()
	object_to_test.add_widget(bet)
	def test_object_structure(self):
	"""
	Function checking the widget display contained all the informations expected
	"""
	assert len(object_to_test) == 1
	assert object_to_test.children[0].odd == "2.0"
	assert object_to_test.children[0].mise == "1000"

	@patch("UrlRequest")
	def test_bet_succeed(self, mock_request):
	"""
	Function checking the function posting the bet is called when the user put
	the right informations
	"""
	object_to_test.children[0].bet()
	assert mock_request.called

	def test_bet_fail(self):
	"""
	Function checking the right error messages are displayed if the user doesn't
	put the right informations
	"""
	object_to_test.children[0].odd = ""
	assert object_to_test.children[0].bet() == "cote absente"
	object_to_test.children[0].odd = "2.0"
	object_to_test.children[0].mise = "1000000"
	assert object_to_test.children[0].bet() == "mise trop élevée"

