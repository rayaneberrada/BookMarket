import json

from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest

from .pages.bestplayers.bestplayerspage import BestPlayerPage
from .pages.bet.betpage import BetPage
from .pages.match.matchpage import MatchPage 
from .pages.matchselection.selectionpages import SportPage, RegionPage, LeaguePage
from .buttons.buttons import GoBackward, SubmitButton 

Builder.load_file('screens/bet/bettingscreen.kv')

class BettingScreen(Screen):
    def __init__(self, screenmanager, user, money, **kwargs):
        super(BettingScreen, self).__init__(**kwargs)
        ###Screens###
        self.screenmanager = screenmanager
        ###Pages###
        self.current_page = 0
        self.pages = [SportPage(self)]
        ###Buttons###
        self.submit = SubmitButton(self.create_view)
        self.backward = GoBackward(self.previous_view)
        ###User infos###
        self.username = user
        self.money = money
        self.sport_chosen = ""

        self.ids.pages.add_widget(self.pages[0])
        self.create_view(None)

    def create_view(self, choice):
        if self.current_page == 0:
            self.update_money()
        elif self.current_page == 1:
            self.sport_chosen = choice
            self.update_view(RegionPage(self, choice))
        elif self.current_page == 2 and self.pages[1].args != "":
            self.update_view(LeaguePage(self, self.pages[1].args))
        elif self.current_page == 2 and self.pages[1].args == "":
            print(self.region_args)
            pop = Popup(title='Invalid Request',
                  content=Label(text='Choisissez au moins une région'),
                  size_hint=(None, None), size=(250, 250))
            pop.open()
        elif self.current_page == 3 and self.pages[1].args != "":
            self.ids.bottom.remove_widget(self.submit)
            self.update_view(MatchPage(self))
        elif self.current_page == 3 and self.match_args == "":
            pop = Popup(title='Invalid Request',
                  content=Label(text='Choisissez au moins un championnat'),
                  size_hint=(None, None), size=(350, 350))
            pop.open()
        elif self.current_page == 5:
            self.ids.pages.remove_widget(self.pages[0])
            self.pages.append(BetPage(self.username))
            self.ids.pages.add_widget(self.pages[1])
            self.ids.bottom.add_widget(self.backward)
        elif self.current_page == 6:
            self.ids.pages.remove_widget(self.pages[0])
            self.pages.append(BestPlayerPage())
            self.ids.pages.add_widget(self.pages[1])
            self.ids.bottom.add_widget(self.backward)
        self.current_page += 1


    def previous_view(self):
        if 5 > self.current_page:
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
            self.pages.pop(1)
            self.current_page == 1
            self.ids.pages.add_widget(self.pages[0]) 

    def update_view(self, page_to_add):
        self.ids.pages.remove_widget(self.pages[self.current_page - 1])
        self.pages.append(page_to_add)
        self.ids.pages.add_widget(self.pages[self.current_page])
        if self.current_page == 1:
            self.ids.bottom.add_widget(self.submit)
            self.ids.bottom.add_widget(self.backward)

    def bets_view(self):
        self.current_page = 5
        self.create_view(None)

    def winners_view(self):
        self.current_page = 6
        self.create_view(None)

    def update_money(self):
        self.ids.amount.text = "Solde: " + str(self.money)

    def logout(self):
        self.screenmanager.display.current = "login"
        while self.current_page != 1:
            self.previous_view()