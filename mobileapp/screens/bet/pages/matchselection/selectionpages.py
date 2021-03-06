"""
This file contain the classes managin the choice of the functionnalities and the process
to request bets depending of the sport/region/league chosen
"""
import functools

from kivy.uix.recycleview import RecycleView
from kivy.network.urlrequest import UrlRequest

from . import selectableLabel

class SportPage(RecycleView):
    """
    This class manage the display and choice of functionnalities and sports we want
    to see depending of the the regions and competitions having bets available for.
    """
    def __init__(self, view_manager, **kwargs):
        super(SportPage, self).__init__(**kwargs)
        self.data = []
        self.next_view = view_manager.create_view
        self.private_view = view_manager.create_private_bets_page
        self.bets_view = view_manager.create_bets_page
        self.winners_view = view_manager.create_winners_page
        #view_manager contain BettingScreen so that we can bind the  page creation functions in it
        #to the buttons created by sport page and are refering to the different functionnalities.
        self.request_json()

    def request_json(self):
        """
        Request on our API the sports avaialbles for betting
        """
        UrlRequest('http://206.189.118.233/sports', self.parse_json)

    def parse_json(self, req, result):
        """
        Parse and add to our view the sports we received in answer and also add the button
        to request all the bets done by the user since the profile exist,the best players
        of the app and the bets created by users.
        """
        self.data = []
        for value in result["sports"]:
            self.data.append({"text" : value['nom'], "name" : value["nom"],
                              "on_press" : functools.partial(self.next_view, value['id'])})
        self.data.append({"text" : "Paris privés", "name" : "privés",
                          "on_press" : functools.partial(self.private_view)})
        self.data.append({"text" : "Historique paris", "name" : "historique",
                          "on_press" : functools.partial(self.bets_view)})
        self.data.append({"text" : "Plus gros gagnants", "name" : "gagnants",
                          "on_press" : functools.partial(self.winners_view)})

class RegionPage(RecycleView):
    """
    Class managing the display of the regions available to search for a sport and the request
    of the leagues related to the regions selected by the user
    """
    def __init__(self, player, sport, **kwargs):
        super(RegionPage, self).__init__(**kwargs)
        self.data = []
        self.player = player
        self.args = ""
        UrlRequest('http://206.189.118.233/{}/regions?matches_available=True'.format(sport),
                   self.parse_json)

    def parse_json(self, req, result):
        """
        Display a selectable widget for each value we get from the response send by our Request
        made in __init__
        """
        for value in result["regions"]:
            self.data.append({"text": value})

class LeaguePage(RecycleView):
    """
    Class managing the display of the leagues related to the regions chosen by the user, and the
    search and display of availables matches and bets related to the leagues selected by the user
    """
    def __init__(self, player, request_args, **kwargs):
        super(LeaguePage, self).__init__(**kwargs)
        self.data = []
        self.player = player
        self.args = ""
        UrlRequest("http://206.189.118.233/{}/competitions?".format(self.player.sport_chosen) +
                   request_args, self.parse_json)

    def parse_json(self, req, result):
        """
        Display a selectable widget for each value we get from the response send by our Request
        made in __init__
        """
        self.data = []
        for value in result["competitions"]:
            self.data.append({"text" : value})
