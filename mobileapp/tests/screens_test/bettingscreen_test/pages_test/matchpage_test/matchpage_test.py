"""
File testing the right behavior of matchpage.py module
"""
from unittest.mock import patch
from unittest.mock import Mock

from kivy.lang.builder import Builder

from screens.bet.pages.match.matchpage import MatchPage, Match

Builder.load_file('tests/screens_test/bettingscreen_test/pages_test/matchpage_test/matchpage_test.kv')

class TestMatch:
    """
    Class checking Match follow the right behavior
    """
    player = Mock()
    player.money = 1000
    player.user = "fake_user"
    object_to_test = Match(player)

    @patch("json.dumps")
    @patch("screens.bet.pages.match.matchpage.UrlRequest")
    def test_bet_succes(self, request_mock, mock_jsonify):
        """
        Check that when called, bet send a request and update properly the money
        of the user depending of the amount that he bets
        """
        respone = {
            "bet":10,
            "succes_message":"Pari ajouté"
        }
        mock_jsonify.return_value = True
        request_mock.return_value = self.object_to_test.update_player(None, respone)
        self.object_to_test.ids.input_home.text = "10"
        self.object_to_test.ids.bet_home.text = "2.35"
        self.object_to_test.bet("Domicile")
        assert request_mock.called
        assert self.object_to_test.screen.money == 990

    @patch("json.dumps")
    @patch("screens.bet.pages.match.matchpage.UrlRequest")
    def test_bet_fail(self, request_mock, mock_jsonify):
        """
        Check that when the match has begun already, the user recevie an error message
        """
        respone = {
            "error_message":"Pari déjà en cours"
        }
        mock_jsonify = True
        request_mock.return_value = self.object_to_test.out_of_date(None, respone)
        self.object_to_test.ids.input_home.text = "10"
        self.object_to_test.ids.bet_home.text = "2.35"
        self.object_to_test.bet("Domicile")
        assert request_mock.called
        assert self.object_to_test.out_of_date(None, respone).content.text == "Pari déjà en cours"

    def test_pop_message(self):
        """
        Check that pop_message display the right string used as parameter
        """
        assert self.object_to_test.pop_message("Exemple").content.text == "Exemple"

    def test_bet_not_number(self):
        """
        Check that when the user doesn't write a number in the input made for betting,
        he receives the related error message
        """
        self.object_to_test.ids.input_home.text = "Nantes"
        self.object_to_test.ids.bet_home.text = "2.35"
        assert self.object_to_test.bet("Domicile").content.text == "La mise doit être un nombre"

    def test_bet_empty(self):
        """
        Check that when the input made for betting is empty, the user receives the related
        error message
        """
        self.object_to_test.ids.input_home.text = ""
        self.object_to_test.ids.bet_home.text = "2.35"
        assert self.object_to_test.bet("Domicile").content.text == "Champ vide"

    def test_bet_too_high(self):
        """
        Check that when the amount the user wants to bet is superior to was he has, he receives
        the related message
        """
        self.object_to_test.ids.input_home.text = "1500"
        self.object_to_test.ids.bet_home.text = "2.35"
        assert self.object_to_test.bet("Domicile").content.text == "Argent insuffisant"

    def test_instantiate_match(self):
        """
        Check that when the match is instantiated with the request response, the informations are
        correctly added to the Match object
        """
        response = {'competition': 'Groupe F', 'cote_dom': '3.05', 'cote_ext': '2.35',
                    'cote_nul': '3.25', 'date': 'Tue, 16 Jun 2020 21:00:00 GMT',
                    'domicile': 'France', 'exterieur': 'Allemagne', 'id': '1684', 'tv': None}

        self.object_to_test.instantiate_match(response)
        assert self.object_to_test.ids.title.text == "Groupe F  Tue, 16 Jun 2020 21:00:00 GMT  "
        assert self.object_to_test.ids.bet_home.text == "3.05 France"
        assert self.object_to_test.ids.bet_draw.text == "3.25 Nul"
        assert self.object_to_test.ids.bet_away.text == "2.35 Allemagne"
        assert len(self.object_to_test.children) == 4

    def test_instantiate_match_without_draw(self):
        """
        Check that when the Match object is instantiated by a response that doesn't have a draw value,
        the widget containing the informations related to draw is removed from the Match object.
        """
        response = {'competition': 'Groupe F', 'cote_dom': '3.05', 'cote_ext': '2.35',
                    'cote_nul': 'None', 'date': 'Tue, 16 Jun 2020 21:00:00 GMT',
                    'domicile': 'France', 'exterieur': 'Allemagne', 'id': '1684', 'tv': None}

        self.object_to_test.instantiate_match(response)
        assert self.object_to_test.ids.title.text == "Groupe F  Tue, 16 Jun 2020 21:00:00 GMT  "
        assert len(self.object_to_test.children) == 3

class TestMatchPage:
    """
    Class checking MatchPage always follow the expected behavior
    """
    @patch("screens.bet.pages.match.matchpage.Match.instantiate_match")
    @patch("screens.bet.pages.match.matchpage.MatchPage.add_widget")
    def test_add_to_view(self, mock_add_widget, mock_match_instantiation):
        """
        Check functions related to the behaviour of the method are called
        """
        mock_add_widget.return_value = print()
        mock_match_instantiation.return_value = print()
        player = Mock()
        player.money = 1000
        player.user = "fake_user"
        MatchPage.screen = player
        MatchPage.add_to_view(MatchPage, None, {"matches":"fake_value"})
        assert mock_add_widget.called
        assert mock_match_instantiation.called
