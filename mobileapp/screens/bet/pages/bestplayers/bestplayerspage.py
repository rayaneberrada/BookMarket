"""
Code used to request and display the biggest winners using the app
"""
import json

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.network.urlrequest import UrlRequest

class BestPlayerPage(GridLayout):
    """
    Class managin the request and display of the biggest winners
    """
    def __init__(self,**kwargs):
        super(BestPlayerPage, self).__init__(**kwargs)
        self.cols = 1
        self.bind(minimum_height=self.setter('height'))
        UrlRequest("http://206.189.118.233/winners", self.parse_json)

    def parse_json(self, req, result):
        """
        Callback from UrlRequest that create a label for each playe it received in the
        request response.
        """
        place = 1
        for value in result["winners"]:
            description = value["nom"] + " est " + str(place) + " avec un total de " + str(value["argent"])
            winner = Label(text=description, size_hint_y= None)
            self.add_widget(winner)
            place += 1
