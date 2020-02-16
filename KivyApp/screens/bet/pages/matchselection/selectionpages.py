import json
import functools

from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.network.urlrequest import UrlRequest

from . import selectableLabel

Builder.load_file('screens/bet/pages/matchselection/selectionpages.kv')

class SportPage(RecycleView):
    def __init__(self, view_manager, **kwargs):
        super(SportPage, self).__init__(**kwargs)
        self.data = []
        self.next_view = view_manager.create_view
        self.bets_view = view_manager.bets_view
        self.winners_view = view_manager.winners_view
        self.request_json(None)

    def request_json(self, arg):
        requestCompetition = UrlRequest('http://127.0.0.1:5000/sports', self.parse_json)

    def parse_json(self, req, result):
        self.data = []
        for value in result["sports"]:
            self.data.append({"text" : value['nom'],"name" : value["nom"], "on_press" : functools.partial(self.next_view, value['nom'])})
        self.data.append({"text" : "Historique paris", "name" : "historique", "on_press" : functools.partial(self.bets_view)})
        self.data.append({"text" : "Plus gros gagnants", "name" : "gagnants", "on_press" : functools.partial(self.winners_view)})

class RegionPage(RecycleView):
    def __init__(self, screen, sport, **kwargs):
        super(RegionPage, self).__init__(**kwargs)
        self.data = []
        self.screen = screen
        self.args = ""
        requestRegions = UrlRequest('http://127.0.0.1:5000/rencontres/{}/regions'.format(sport), self.parse_json)

    def parse_json(self, req, result):
        for value in result["regions"]:
            self.data.append({"text": value})

class LeaguePage(RecycleView):
    def __init__(self, screen, request_args, **kwargs):
        super(LeaguePage, self).__init__(**kwargs)
        self.data = []
        self.screen = screen
        self.args = ""
        requestLeagues = UrlRequest("http://127.0.0.1:5000/rencontres/{}/competitions?".format(self.screen.sport_chosen) + request_args, self.parse_json)

    def parse_json(self, req, result):
        self.data = []
        for value in result["competitions"]:
            self.data.append({"text" : value})

