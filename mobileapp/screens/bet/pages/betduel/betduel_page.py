
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
    def __init__(self, screen, **kwargs):
        super(PrivateBetPage, self).__init__(**kwargs)
        self.screen = screen
        self.bind(minimum_height=self.setter('height'))
        UrlRequest('http://206.189.118.233/rencontres?competition=private', on_success=self.add_to_view,
                          on_failure=self.fail)

    def add_to_view(self, req, result):
        """
        Instantiate a Match for each match contained in the response sent back by the UrlRequest
        and add it to the grid of MatchPage to be displayed on our screen view
        """
        for value in result["matches"]:
            match = PrivateMatch(self.screen)
            match.instantiate_match(value)
            self.add_widget(match)

    def fail(self):
        print("it failed")

class PrivateMatch(GridLayout):
    """
    Class building and managinf  functionnalities related to the matches
    """
    def __init__(self, screen, **kwargs):
        super(PrivateMatch, self).__init__(**kwargs)
        self.screen = screen
        self.odd = None
        self.team_chosen = None
        self.match_id = None

    def bet(self):
        """
        Look for the informations contained in the inputs and eitheir display an error message
        if someting is missing, or send a request to the server to save the bet made by the user.
        """

        if self.ids.input_amount:
            if str(self.ids.input_amount).isdigit() and int(self.ids.input_amount) >= 1 :
                self.ids.input_amount = int(self.ids.input_amount)
                if self.screen.money >= self.ids.input_amount:
                    headers = {"Content-Type": "application/json"}
                    params = json.dumps({"bet": self.ids.input_amount, "odd":self.odd, "user_id": self.screen.username,
                                         "match_id": self.match_id, "team_selected": self.team_chosen})
                    UrlRequest('http://206.189.118.233/bets', on_success=self.update_player,
                               on_failure=self.out_of_date, req_body=params, req_headers=headers)
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
        tv = value["tv"] if value["tv"] is not None else ""
        self.team_chosen = value["domicile"] if value["cote_dom"] else (value["exterieur"] if value["cote_ext"] else "Nul")
        self.odd = "1"
        for odd in [value["cote_dom"], value["cote_ext"], value["cote_nul"]]:
            self.odd = odd if odd != "None" else self.odd

        self.match_id = value["id"]
        self.ids.title.text = value["region"] + "  " + value["date"] + "  " + tv
        self.ids.match.text = value["domicile"] + " contre " + value["exterieur"]
        self.ids.bet.text = self.odd + " " + self.team_chosen
        self.ids.mise.text = "mise maximale: " + str(value["mise"])


    def update_player(self, req, result):
        """
        Update the amount available to the player if the bet has been accepted
        """
        if "succes_message" in result:
            self.screen.money -= result["bet"]
            self.screen.update_money()
            self.pop_message(result["succes_message"])

    def out_of_date(self, req, result):
        """
        Display an error message if the player try to bet on a game that has
        already begun
        """
        if "error_message" in result:
            pop = Popup(title='Invalid Form',
                        content=Label(text=result["error_message"]),
                        size_hint=(None, None), size=(250, 250))

            pop.open()
            return pop

    def pop_message(self, message):
        """
        Display a message to the user
        """
        pop = Popup(title='Invalid Form',
                    content=Label(text=message),
                    size_hint=(None, None), size=(250, 250))

        pop.open()
        return pop