from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.network.urlrequest import UrlRequest

Builder.load_file('screens/bet/pages/bestplayers/bestplayerspage.kv')

class BestPlayerPage(GridLayout):
    def __init__(self,**kwargs):
        super(BestPlayerPage, self).__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))
        request_bets = UrlRequest("http://127.0.0.1:5000/winners", self.parse_json)

    def parse_json(self, req, result):
        place = 1
        for value in result["winners"]:
            description = value["nom"] + " est " + str(place) + " avec un total de " + str(value["argent"])
            winner = Label(text=description, size_hint_y= None)
            self.add_widget(winner)
            place += 1