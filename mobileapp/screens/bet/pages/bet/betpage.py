"""
This code control the functionnality to search and display the best players of the app
"""
from kivy.uix.gridlayout import GridLayout
from kivy.network.urlrequest import UrlRequest

class BetPage(GridLayout):
    """
    Class mangaging the display and control of the Bet objects
    """
    def __init__(self, player, search_parameters, **kwargs):
        super(BetPage, self).__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))
        self.search_parameters = search_parameters
        request_bets = UrlRequest("http://206.189.118.233/{}/bets".format(player.username), self.parse_json)

    def parse_json(self, req, result):
        """
        Parse every bet asked from our UrlRequest and add them to BetPage to be displayed
        in our app view.
        """
        for value in result["bets"]:
            if value["match_infos"]["resultat_id"] != value["equipe_pariee"] and value["verifie"] == 1:
                color = (0.6, 0, 0, 1)
            elif value["verifie"] == 1:
                color = (0, 0.6, 0, 1)
            else:
                color = (0.500, 0.500, 0.500, 1)
            bet = Bet(color, value)
            if not self.search_parameters:
                self.add_widget(bet)
            else:
                if self.search_parameters.lower() in bet.ids.title.text.lower():
                    self.add_widget(bet)
                else:
                    continue

class Bet(GridLayout):
    """
    Manage the informatiosn and functionnalities related to the bets made by the user
    """
    def __init__(self, color, value, **kwargs):
        self.color = color
        super(Bet, self).__init__(**kwargs)
        self.instantiate(value)

    def instantiate(self, value):
        """
        Add to our Bet widget the information received from the request made to the API.
        The attributes containing those informations have been discribed in betpage.kv.
        """
        team_chosen = "Domicile" if value["equipe_pariee"] == 1 else("Exterieur" if value["equipe_pariee"] == 2 else "Nul")
        if value["match_infos"]["resultat_id"] == 1:
            result = "Résultat: " + value["match_infos"]["equipe_domicile"]
        elif value["match_infos"]["resultat_id"] == 2:
            result = "Résultat: " + value["match_infos"]["equipe_exterieure"]
        elif value["match_infos"]["resultat_id"] == 3:
            result = "Nul"
        else:
            result = "Match pas encore joué"

        if self.color == ((0.6, 0, 0, 1)):
            self.ids.earning.text = "   Pertes: -" + str(value["mise"])
        elif self.color == ((0, 0.6, 0, 1)):
            self.ids.earning.text = "  Gains: +" + str(int(value["mise"]*float(value["cote"])))
        else:
            self.ids.earning.text = "   Gains potentiels: +" + str(int(value["mise"]*float(value["cote"])))

        self.ids.title.text = value["match_infos"]["equipe_domicile"] + " vs " + value["match_infos"]["equipe_exterieure"]
        self.ids.date.text = "   Date match: " + value["match_infos"]["date_affrontement"]
        self.ids.bet.text = "   Pari: " + str(value["mise"]) + " parié sur " + team_chosen + " avec une cote de " + str(value["cote"])
        self.ids.result.text = "   " + result
