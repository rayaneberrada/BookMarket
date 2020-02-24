"""
File testing the right behavior of betpage.py
"""
from unittest.mock import patch

from kivy.lang.builder import Builder

from screens.bet.pages.bet.betpage import BetPage, Bet

Builder.load_file('tests/screens_test/bettingscreen_test/pages_test/betpage_test/betpage_test.kv')

class TestBetPage:
    """
    Class checking BetPage follow the expected behavior
    """
    response = {"bets":[{'cote': '1.35', 'verifie':0, 'mise':50,
                         'date_enregistrement': 'Thu, 20 Feb 2020 18:35:13 GMT',
                         'equipe_pariee': 1, 'id': 42,
                         'match_infos': {'competition': 'Groupe E',
                                         'date_affrontement': 'Mon, 15 Jun 2020 21:00:00 GMT',
                                         'equipe_domicile': 'Espagne',
                                         'equipe_exterieure': 'Suède', 'resultat_id': None}}]}

    @patch("screens.bet.pages.bet.betpage.BetPage.add_widget")
    def test_parser(self, mock_add_widget):
        """
        Check the parser use the function to add the Bet object to BetPage
        """
        BetPage.parse_json(BetPage, None, self.response)
        assert mock_add_widget.called

class TestBet:
    """
    Class checking Bet follow the expected behavior
    """
    response = {'cote': '1.35', 'verifie':0, 'mise':50,
                'date_enregistrement': 'Thu, 20 Feb 2020 18:35:13 GMT',
                'equipe_pariee': 1, 'id': 42,
                'match_infos': {'competition': 'Groupe E',
                                'date_affrontement': 'Mon, 15 Jun 2020 21:00:00 GMT',
                                'equipe_domicile': 'Espagne', 'equipe_exterieure': 'Suède',
                                'resultat_id': None}}

    def test_instantiation(self):
        """
        Check that when instantiated, the informations are correctly added to the widget.
        """
        bet = Bet((0.500, 0.500, 0.500, 1), self.response)
        assert bet.ids.earning.text == "   Gains potentiels: +67.5"
        assert bet.ids.title.text == "Espagne vs Suède"
        assert bet.ids.date.text == "   Date match: Mon, 15 Jun 2020 21:00:00 GMT"
        assert bet.ids.bet.text == "   Pari: 50 parié sur Domicile avec une cote de 1.35"
        assert bet.ids.result.text == "   Match pas encore joué"
