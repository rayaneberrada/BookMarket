import json

from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest

from .pages.bestplayers.bestplayerspage import BestPlayerPage
from .pages.bet.betpage import BetPage
from .pages.match.matchpage import MatchPage
from .pages.matchselection.selectionpages import SportPage, RegionPage, LeaguePage
from .buttons.buttons import GoBackward, SubmitButton

class BettingScreen(Screen):
    def __init__(self, screenmanager, user, money, **kwargs):
        super(BettingScreen, self).__init__(**kwargs)
        ###Screens###
        self.screenmanager = screenmanager
        ###Pages###
        self.current_page = 0
        self.pages = []
        ###Buttons###
        self.submit = SubmitButton(self.create_view)
        self.backward = GoBackward(self.previous_view)
        ###User infos###
        self.username = user
        self.money = money
        self.sport_chosen = ""

        self.create_view(None)

    def create_view(self, choice):
        self.sport_chosen = choice if choice else self.sport_chosen
        page = {
            0: self.create_sport_page,
            1: self.create_region_page,
            2: self.create_league_page,
            3: self.create_match_page
        }.get(self.current_page)
        page()

    def create_sport_page(self):
        self.pages.append(SportPage(self))
        self.ids.pages.add_widget(self.pages[0])
        self.update_money()
        self.current_page += 1

    def create_region_page(self):
        self.update_view(RegionPage(self, self.sport_chosen))
        self.update_money()
        self.current_page += 1

    def create_league_page(self):
        regions_request_args = self.pages[1].args
        if  regions_request_args != "":
            self.update_view(LeaguePage(self, self.pages[1].args))
            self.update_money()
            self.current_page += 1
        else:
            self.empty_args()

    def create_match_page(self):
        league_request_args = self.pages[2].args
        if  league_request_args != "":
            self.update_view(MatchPage(self))
            self.ids.bottom.remove_widget(self.submit)
            self.update_money()
            self.current_page += 1
        else:
            self.empty_args()

    def create_bets_page(self):
        self.ids.pages.remove_widget(self.pages[0])
        self.pages.append(BetPage(self.username))
        self.ids.pages.add_widget(self.pages[1])
        self.ids.bottom.add_widget(self.backward)
        self.current_page = 9

    def create_winners_page(self):
        self.ids.pages.remove_widget(self.pages[0])
        self.pages.append(BestPlayerPage())
        self.ids.pages.add_widget(self.pages[1])
        self.ids.bottom.add_widget(self.backward)
        self.current_page = 9

    def update_view(self, page_to_add):
        self.ids.pages.remove_widget(self.pages[self.current_page - 1])
        self.pages.append(page_to_add)
        self.ids.pages.add_widget(self.pages[self.current_page])
        if self.current_page == 1:
            self.ids.bottom.add_widget(self.submit)
            self.ids.bottom.add_widget(self.backward)

    def empty_args(self):
            pop = Popup(title='Invalid Request',
                  content=Label(text='Saisissez une réponse'),
                  size_hint=(None, None), size=(250, 250))
            pop.open()

    def previous_view(self):
        if self.current_page != 9:
            self.ids.pages.remove_widget(self.pages[self.current_page - 1])
            self.pages.pop(self.current_page - 1)
            self.current_page -= 1
            self.ids.pages.add_widget(self.pages[self.current_page - 1])
            if self.current_page == 1:
                self.ids.bottom.remove_widget(self.submit)
                self.ids.bottom.remove_widget(self.backward)
            elif self.current_page == 3:
                self.ids.bottom.add_widget(self.submit)
        else:
            self.ids.pages.remove_widget(self.pages[1])
            self.ids.bottom.remove_widget(self.backward)
            self.pages.pop(1)
            self.current_page == 1
            self.ids.pages.add_widget(self.pages[0])

    def update_money(self):
        self.ids.amount.text = "Solde: " + str(self.money)

    def logout(self):
        self.screenmanager.display.current = "login"