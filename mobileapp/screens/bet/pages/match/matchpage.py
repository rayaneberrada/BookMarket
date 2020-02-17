import json

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.network.urlrequest import UrlRequest

class MatchPage(GridLayout):
    def __init__(self, screen, **kwargs):
        super(MatchPage, self).__init__(**kwargs)
        self.league_args = screen.pages[2].args
        self.screen = screen
        self.bind(minimum_height=self.setter('height'))
        self.create_grid_matches()


    def add_to_view(self, req, result):
        print(result)
        for value in result["matches"]:
            tv = value["tv"] if value["tv"] != None else ""
            match = Match(self.screen)
            match.id = value["id"]
            match.ids.title.text = value["competition"] + "  " + value["date"] + "  " + tv
            match.ids.bet_home.text = value["cote_dom"] + " " + value["domicile"]
            match.ids.bet_draw.text = value["cote_nul"] + " Nul"
            match.ids.bet_away.text = value["cote_ext"] + " " + value["exterieur"]
            if value["cote_nul"] == "None":
                match.remove_widget(match.ids.draw)
            self.add_widget(match)

    def create_grid_matches(self):
        requestMatches = UrlRequest('http://127.0.0.1:5000/rencontres?' + self.league_args, self.add_to_view)
        return self

class Match(GridLayout):
    def __init__(self, screen, **kwargs):
        super(Match, self).__init__(**kwargs)
        self.screen = screen

    def bet(self, button_text):
        if button_text == "Domicile":
            input_amount = self.ids.input_home.text
            odd = self.ids.bet_home.text.split()[0]
            team_selected = 1
        elif button_text =="Extérieur":
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
                    params = json.dumps({"bet": input_amount, "odd":odd, "user_id": self.screen.username, "match_id": self.id, "team_selected": team_selected})
                    req = UrlRequest('http://127.0.0.1:5000/bets', on_success=self.update_player, on_failure=self.out_of_date,
                req_body=params, req_headers=headers)
                else:
                    self.pop_message("argent insuffisant")
            else:
                self.pop_message("La mise doit être un nombre")
        else:
            self.pop_message("Champ vide")

    def update_player(self, req, result):
        if "succes_message" in result:
            self.screen.money -= result["bet"]
            self.screen.update_money()
            self.pop_message(result["succes_message"])

    def out_of_date(self, req, result):
        if "error_message" in result:
            pop = Popup(title='Invalid Form',
                          content=Label(text=result["error_message"]),
                          size_hint=(None, None), size=(250, 250))

            pop.open()
        else:
            print(result)

    def pop_message(self, message):
        pop = Popup(title='Invalid Form',
                      content=Label(text=message),
                      size_hint=(None, None), size=(250, 250))

        pop.open()