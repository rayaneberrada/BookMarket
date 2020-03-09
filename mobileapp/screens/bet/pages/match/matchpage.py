"""
This file manage the display of the match requested by the user and to send
the request when the user want to bet on one of the match displayed
"""
import json

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.network.urlrequest import UrlRequest

class MatchPage(GridLayout):
    """
    Class managing and containing the matcheds requested by the user
    """
    def __init__(self, screen, **kwargs):
        super(MatchPage, self).__init__(**kwargs)
        self.league_args = screen.pages[2].args
        self.screen = screen
        self.bind(minimum_height=self.setter('height'))
        UrlRequest('http://206.189.118.233/rencontres?' + self.league_args, self.add_to_view)


    def add_to_view(self, req, result):
        """
        Instantiate a Match for each match contained in the response sent back by the UrlRequest
        and add it to the grid of MatchPage to be displayed on our screen view
        """
        for value in result["matches"]:
            match = Match(self.screen)
            match.instantiate_match(value)
            self.add_widget(match)

class Match(GridLayout):
    """
    Class building and managinf  functionnalities related to the matches
    """
    def __init__(self, screen, **kwargs):
        super(Match, self).__init__(**kwargs)
        self.screen = screen

    def bet(self, button_text):
        """
        Look for the informations contained in the inputs and eitheir display an error message
        if someting is missing, or send a request to the server to save the bet made by the user.
        """
        if button_text == "Domicile":
            input_amount = self.ids.input_home.text
            odd = self.ids.bet_home.text.split()[0]
            team_selected = 1
        elif button_text == "Extérieur":
            input_amount = self.ids.input_away.text
            odd = self.ids.bet_away.text.split()[0]
            team_selected = 2
        elif button_text == "Nul":
            input_amount = self.ids.input_draw.text
            odd = self.ids.bet_draw.text.split()[0]
            team_selected = 3

        if input_amount:
            if input_amount.isdigit():
                input_amount = int(input_amount)
                if self.screen.money >= input_amount:
                    headers = {"Content-Type": "application/json"}
                    params = json.dumps({"bet": input_amount, "odd":odd, "user_id": self.screen.username,
                                         "match_id": self.id, "team_selected": team_selected})
                    UrlRequest('http://206.189.118.233/bets', on_success=self.update_player,
                               on_failure=self.out_of_date, req_body=params, req_headers=headers)
                else:
                    return self.pop_message("Argent insuffisant")
            else:
                return self.pop_message("La mise doit être un nombre")
        else:
            return self.pop_message("Champ vide")

    def instantiate_match(self, value):
        """
        Instantiate the match grid informations to be displayer in our view.
        Those values our defined in our kv file related to matchpage.
        """
        tv = value["tv"] if value["tv"] is not None else ""
        self.id = value["id"]
        self.ids.title.text = value["competition"] + "  " + value["date"] + "  " + tv
        self.ids.bet_home.text = value["cote_dom"] + " " + value["domicile"]
        self.ids.bet_draw.text = value["cote_nul"] + " Nul"
        self.ids.bet_away.text = value["cote_ext"] + " " + value["exterieur"]
        if value["cote_nul"] == "None":
            self.remove_widget(self.ids.draw)

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

    def create_bet(self):
        """
        Instantiate the popup widget with the informations of the bet the player want
        to use as a model
        """
        bet_interface = BetCreation(self.screen.username, self.screen.money, self.id, self.ids.bet_home.text,
                                    self.ids.bet_draw.text, self.ids.bet_away.text)
        bet_interface.id = self.id
        bet_interface.ids.home.text = self.ids.bet_home.text
        bet_interface.ids.draw.text = self.ids.bet_draw.text
        bet_interface.ids.away.text = self.ids.bet_away.text
        bet_interface.height = self.height * 4
        bet_interface.width = self.width
        bet_interface.open()
        return bet_interface

class BetCreation(Popup):
    """
    Create a popup that the player can use to create a bet that other players will
    be able to bet against
    """
    def __init__(self, username, money, bet_id, home, draw, away, **kwargs):
        super(BetCreation, self).__init__(**kwargs)
        self.username = username
        self.user_money = money
        self.bet_id = bet_id
        self.ids.home.text = home
        self.ids.away.text = away
        if "None" in draw:
            print("yes")
            self.ids.button_choice.remove_widget(self.ids.draw)
        else:
            self.ids.draw.text = draw

    def save_bet(self):
        if self.ids.input_money.text.isdigit() and self.ids.input_odd.text:
            money = int(self.ids.input_money.text)
            try:
                odd = float(self.ids.input_odd.text.replace(",","."))
                if 1.0 > odd:
                    raise ValueError
                if odd*money > self.user_money:
                    self.ids.error.text = "Vous n'avez pas les fonds suffisants"
                else:
                    selection = 1
                    for widget in reversed(self.ids.button_choice.children):
                        if widget.state != "down":
                            self.ids.error.text = "Vous devez choisir un résultat"
                            selection += 1
                            continue
                        else:
                            self.ids.error.text = ""
                            headers = {"Content-Type": "application/json"}
                            params = json.dumps({"bet":int(money), "odd":odd, "user_id": self.username,
                                        "match_id": self.id, "team_selected": selection})
                            UrlRequest('http://206.189.118.233/betexchange', on_success=self.dismiss, on_failure=self.fail_to_save,
                                    req_body=params, req_headers=headers)
            except ValueError:
                self.ids.error.text = "Vous devez entrer un nombre entier ou décimal supérieur à 1 dans côte"
        else:
            self.ids.error.text = "Vous devez entrer un nombre entier supérieur à 0 dans mise"



    def fail_to_save(self, req, result):
        self.dismiss()
        pop = Popup(title='Invalid Form',
                    content=Label(text=result["succes_message"]),
                    size_hint=(None, None), size=(250, 250))
        pop.open()
        return pop
