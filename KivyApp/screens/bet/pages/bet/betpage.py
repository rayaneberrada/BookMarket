from kivy.lang.builder import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.network.urlrequest import UrlRequest

Builder.load_file('screens/bet/pages/bet/betpage.kv')

class BetPage(GridLayout):
    def __init__(self, user,**kwargs):
        super(BetPage, self).__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))
        request_bets = UrlRequest("http://127.0.0.1:5000/{}/bets".format(user), self.parse_json)

    def parse_json(self, req, result):
        for value in result["bets"]:
            team_chosen = "Domicile" if value["equipe_pariee"] == 1 else ("Exterieur" if value["equipe_pariee"] == 2 else "Nul")
            if value["match_infos"]["resultat_id"] == 1:
                result = value["equipe_domicile"]
            if value["match_infos"]["resultat_id"] == 2:
                result = value["equipe_exterieure"]
            if value["match_infos"]["resultat_id"] == 3:
                result = "Nul"
            else:
                result = "Match pas encore joué"

            if value["match_infos"]["resultat_id"] != value["equipe_pariee"] and value["verifie"] == 1:
                bet = Bet((0.6, 0, 0, 1))
                bet.ids.earning.text = "   Pertes: -" + str(value["mise"])
            elif value["verifie"] == 1:
                bet = Bet((0, 0.6, 0, 1))
                bet.ids.earning.text = "  Gains: +" + str(value["mise"]*float(value["cote"]))
            else:
                bet = Bet((0.500, 0.500, 0.500, 1))
                bet.ids.earning.text = "   Gains potentiels: +" + str(value["mise"]*float(value["cote"]))

            bet.ids.title.text = value["match_infos"]["equipe_domicile"] + " vs " + value["match_infos"]["equipe_exterieure"]
            bet.ids.date.text = "   Date match: " + value["match_infos"]["date_affrontement"]
            bet.ids.bet.text = "   Pari: " + str(value["mise"]) + " parié sur " + team_chosen + " avec une cote de " + str(value["cote"])
            bet.ids.result.text = "   " + result

            self.add_widget(bet)

class Bet(GridLayout):
    def __init__(self, color, **kwargs):
        self.color = color
        super(Bet, self).__init__(**kwargs)