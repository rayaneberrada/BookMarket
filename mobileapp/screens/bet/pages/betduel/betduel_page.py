
"""
This file manage the display of the match requested by the user and to send
the request when the user want to bet on one of the match displayed
"""
import json

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.network.urlrequest import UrlRequest

class PrivateBetPage(GridLayout):
    """
    Class managing and containing the matcheds requested by the user
    """
    def __init__(self, player, search_params, **kwargs):
        super(PrivateBetPage, self).__init__(**kwargs)
        self.player = player
        self.search_params = search_params
        self.bind(minimum_height=self.setter('height'))
        UrlRequest('http://206.189.118.233/0/rencontres?private=True', on_success=self.add_to_view,
                    on_failure=self.display_message, on_error=self.display_message,)

    def add_to_view(self, req, result):
        """
        Instantiate a Match for each match contained in the response sent back by the UrlRequest
        and add it to the grid of MatchPage to be displayed on our player view
        """
        for value in result["matches"]:
            match = PrivateMatch(self.player)
            match.instantiate_match(value)
            if not self.search_params:
                self.add_widget(match)
                match.height = self.height * 2
            else:
                if self.search_params.lower() in match.ids.match.text.lower():
                    self.add_widget(match)
                    match.height = self.height * 2
                else:
                    continue

    def display_message(self, req, result):
        """
        If success we don't need a message because widget will already be displayed
        Otherwiser display an error message if returned by the server, or a connexion issue
        if the server couldn't be reached
        """
        if "error_message" in result:
            return self.popup_message(result["error_message"])
        else:
            return self.popup_message("Connexion avec le serveur impossible")

    def popup_message(self, message):
        """
        Popup displayed to the user showing the message used in argument.
        """
        message = Popup(title="",
                        content=Label(text=message),
                        size_hint=(None, None), size=(self.width*0.7, self.height*0.4))
        message.open()
        return message.content.text
        #It returns text to help for testing

class PrivateMatch(GridLayout):
    """
    Class building and managinf  functionnalities related to the matches
    """
    def __init__(self, player, **kwargs):
        super(PrivateMatch, self).__init__(**kwargs)
        self.player = player
        self.odd = None
        self.team_chosen = None
        self.match_id = None
        self.max_bet = None

    def bet(self):
        """
        Look for the informations contained in the inputs and eitheir display an error message
        if someting is missing, or send a request to the server to save the bet made by the user.
        """

        if self.ids.input_amount.text:
            if self.ids.input_amount.text.isdigit() and int(self.ids.input_amount.text) >= 1 :
                bet = int(self.ids.input_amount.text)
                if self.player.money >= bet:
                    if self.max_bet >= bet:
                        self.max_bet -= int(bet)
                        self.ids.mise.text = "mise maximale: " + str(self.max_bet)
                        headers = {"Content-Type": "application/json"}
                        params = json.dumps({"bet": bet, "odd":self.odd, "user_id": self.player.username,
                                             "match_id": self.match_id, "team_selected": self.team_chosen, "private": True})
                        UrlRequest('http://206.189.118.233/bet', on_success=self.update_player,
                                   on_failure=self.out_of_date, req_body=params, req_headers=headers)
                    else:
                        return self.pop_message("Mise trop élevée")
                else:
                    return self.pop_message("Argent insuffisant")
            else:
                return self.pop_message("La mise doit être un entier non nul")
        else:
            return self.pop_message("Champ vide")

    def instantiate_match(self, value):
        """
        Instantiate the match grid informations to be displayer in our view.
        Those values our defined in our kv file related to matchpage.
        """
        self.max_bet = value["mise"]
        tv = value["tv"] if value["tv"] is not None else ""
        self.team_chosen = 1 if value["cote_dom"] != "None" else (2 if value["cote_ext"] != "None" else 3)
        bet_team_name = value["domicile"] if value["cote_dom"] != "None" else (value["exterieur"] if value["cote_ext"] != "None" else "Nul")
        self.odd = "1"
        for odd in [value["cote_dom"], value["cote_ext"], value["cote_nul"]]:
            self.odd = odd if odd != "None" else self.odd

        self.match_id = value["id"]
        self.ids.title.text = value["region"] + "  " + value["date"] + "  " + tv
        self.ids.match.text = value["domicile"] + " contre " + value["exterieur"]
        self.ids.bet.text = self.odd + " " + bet_team_name
        self.ids.mise.text = "mise maximale: " + str(self.max_bet)


    def update_player(self, req, result):
        """
        Update the amount available to the player if the bet has been accepted
        """
        if "succes_message" in result:
            self.player.money -= result["bet"]
            self.player.ids.amount.text = "Solde: " + str(self.player.money)
            self.pop_message(result["succes_message"])

    def out_of_date(self, req, result):
        """
        Display an error message if the player try to bet on a game that has
        already begun
        """
        if "error_message" in result:
            pop = Popup(title='',
                        content=Label(text=result["error_message"]),
                        size_hint=(None, None), size=(self.width * 0.7, self.height * 0.4))

            pop.open()
            return pop

    def pop_message(self, message):
        """
        Display a message to the user
        """
        pop = Popup(title='',
                    content=Label(text=message),
                    size_hint=(None, None), size=(self.width * 0.7, self.height * 0.4))

        pop.open()
        return pop
