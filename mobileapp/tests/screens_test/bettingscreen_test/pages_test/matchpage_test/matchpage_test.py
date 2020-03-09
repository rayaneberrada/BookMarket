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
    Class checking Match are correctly created
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
        assert len(self.object_to_test.children) == 5

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
        assert len(self.object_to_test.children) == 4

    def test_popup_bet_creation(self):
        """
        Check that the popu contained the expected row and values associated
        """
        bet_creator = self.object_to_test.create_bet()
        assert bet_creator.ids.home.group == "bet_choice"
        assert bet_creator.ids.away.group == "bet_choice"
        assert len(bet_creator.ids) == 9
        assert bet_creator.ids.input_odd
        assert bet_creator.ids.input_money
        assert bet_creator.ids.save

    @patch("json.dumps")
    @patch("screens.bet.pages.match.matchpage.UrlRequest")
    def test_popup_bet_creation_fail(self, mock_request, mock_dump):
        """
        Check the right error messages are displayed when entries are not properly
        filled
        """
        bet_creator = self.object_to_test.create_bet()
        mock_request.return_value = bet_creator.fail_to_save(None, { "succes_message": "Pari enregistré"})
        mock_dump.return_value = True
        bet_creator.save_bet()
        assert bet_creator.ids.error.text == "Vous devez entrer un nombre entier supérieur à 0 dans mise"
        bet_creator.ids.input_money.text = "100"
        bet_creator.save_bet()
        assert bet_creator.ids.error.text == "Vous devez entrer un nombre entier supérieur à 0 dans mise"
        bet_creator.ids.input_odd.text = "azdadz"
        bet_creator.save_bet()
        assert bet_creator.ids.error.text == "Vous devez entrer un nombre entier ou décimal supérieur à 1 dans côte"
        bet_creator.ids.input_odd.text = "0.5"
        assert bet_creator.ids.error.text == "Vous devez entrer un nombre entier ou décimal supérieur à 1 dans côte"
        bet_creator.ids.input_odd.text = "100"
        bet_creator.save_bet()
        assert bet_creator.ids.error.text == "Vous n'avez pas les fonds suffisants"
        bet_creator.ids.input_odd.text = "2"
        bet_creator.save_bet()
        assert bet_creator.ids.error.text == "Vous devez choisir un résultat"
        bet_creator.ids.button_choice.children[0].state = "down"
        bet_creator.save_bet()
        assert mock_request.called
        assert mock_request.return_value.content.text == "Pari enregistré"

    @patch("json.dumps")
    @patch("screens.bet.pages.match.matchpage.BetCreation.dismiss")
    @patch("screens.bet.pages.match.matchpage.UrlRequest")
    def test_popup_bet_creation_succeed(self, mock_request, mock_quit, mock_dump):
        """
        Check request is send when all entries are filled with expected values
        and that the popup close
        """
        bet_creator = self.object_to_test.create_bet()
        mock_request.return_value = bet_creator.dismiss()
        bet_creator.ids.button_choice.children[0].state = "down"
        bet_creator.ids.input_odd.text = "3"
        bet_creator.ids.input_money.text = "50"
        bet_creator.save_bet()
        print(bet_creator.ids.error.text)
        assert mock_request.called
        assert mock_quit.called

class TestMatchPage:
    """
    Class checking MatchPage correctly add the matches and display them
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
