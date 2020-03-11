"""
File testing the right behavior of betpage.py
"""

from unittest.mock import Mock, patch
import datetime

from kivy.lang.builder import Builder

from screens.bet.pages.betduel.betduel_page import PrivateBetPage

Builder.load_file('tests/screens_test/bettingscreen_test/pages_test/betduel_test.kv')

class TestBetDuelPage:
    player = Mock()
    player.money = 1000
    player.user = "fake_user"
    object_to_test = PrivateBetPage(player, None)
    bet = {"matches": [{'cote_nul': 'None', 'domicile': 'Écosse', 'cote_dom': 'None', 'exterieur': 'France',
           'cote_ext': '1.20', 'date': str(datetime.datetime(2020, 3, 8, 16, 0)), 'mise': 100, 'tv': 'FRANCE2',
           'id': '741', 'competition': 'Matchs', 'region': 'Tournoi des 6 Nations', 'sport': 2}]}
    object_to_test.add_to_view(None, bet)

    def test_object_structure(self):
        """
        Function checking the widget display contained all the informations expected
        """
        print(self.object_to_test.children[0])
        assert len(self.object_to_test.children) == 1
        assert len(self.object_to_test.children[0].ids) == 5
        assert self.object_to_test.children[0].ids.title.text == "Tournoi des 6 Nations  2020-03-08 16:00:00  FRANCE2"
        assert self.object_to_test.children[0].ids.match.text == "Écosse contre France"
        assert self.object_to_test.children[0].ids.bet.text  == "1.20 France"
        assert self.object_to_test.children[0].ids.mise.text == "mise maximale: 100"

    def test_bet_fail(self):
        """
        Function checking the right error messages are displayed if the user doesn't
        put the right informations
        """
        self.object_to_test.children[0].ids.input_amount.text = ""
        assert self.object_to_test.children[0].bet().content.text == "Champ vide"
        self.object_to_test.children[0].ids.input_amount.text = "Not a number"
        assert self.object_to_test.children[0].bet().content.text == "La mise doit être un entier non nul"
        self.object_to_test.children[0].ids.input_amount.text = "1000000"
        assert self.object_to_test.children[0].bet().content.text == "Argent insuffisant"

    @patch("json.dumps")
    @patch("screens.bet.pages.betduel.betduel_page.UrlRequest")
    def test_bet_succeed(self, mock_request, mock_parameters):
        """
        Function checking the function posting the bet is called when the user put
        the right informations
        """
        mock_parameters.return_value = True
        self.object_to_test.children[0].ids.input_amount.text = "10"
        self.object_to_test.children[0].bet()
        assert mock_request.called