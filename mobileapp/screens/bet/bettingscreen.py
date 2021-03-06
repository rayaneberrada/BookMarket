"""
This file contain the class managing and displaying all the functionnalities of the
application.
To manage the visual display of the betting screen, check bettingscreen.kv.
"""
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout

from  screens.bet.pages.betduel.betduel_page import PrivateBetPage
from  screens.bet.pages.bestplayers.bestplayerspage import BestPlayerPage
from  screens.bet.pages.bet.betpage import BetPage
from  screens.bet.pages.match.matchpage import MatchPage
from  screens.bet.pages.matchselection.selectionpages import SportPage, RegionPage, LeaguePage
from  screens.bet.buttons.buttons import GoBackward, SubmitButton

class BettingScreen(Screen):
    """
    Class managing the pages that display the different functionnalities of the app.
    The main one being to chose which sport we want to display bets from.
    """
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
        self.sport_chosen = None
        ###Search Input###
        self.search = None
        ###Matches returned###
        self.matches_widgets = []

        self.create_view(None)

    def create_view(self, choice):
        """
        Depending of the current_page value, call the function creating the page
        to display the related functionnality
        """
        self.ids.amount.text = "Solde: " + str(self.money)
        self.sport_chosen = choice if choice else self.sport_chosen
        #If user doesn't change first chocie sport, sport chosen stay the same
        page = {
            0: self.create_sport_page,
            1: self.create_region_page,
            2: self.create_league_page,
            3: self.create_match_page,
            4: self.create_private_bets_page
        }.get(self.current_page)()

    def create_sport_page(self):
        """
        Create the page to chose the sports to get bets from or chose between other
        functionnalities
        """
        self.pages.append(SportPage(self))
        self.ids.pages.add_widget(self.pages[0])
        self.current_page += 1

    def create_region_page(self):
        """
        Create the page displaying all the regions related to the sport chosen.
        The user can then chose which regions he wants to display leagues from.
        """
        self.update_view(RegionPage(self, self.sport_chosen))
        self.current_page += 1

    def create_league_page(self):
        """
        Create the page displaying all the leagues related to the regions chosen.
        The user can then chose which leagues he wants to display matches from.
        """
        regions_request_args = self.pages[1].args
        if  regions_request_args != "":
            self.update_view(LeaguePage(self, self.pages[1].args))
            self.current_page += 1
        else:
            self.empty_args()

    def create_match_page(self):
        """
        Create the page displaying all the match related to the leagues chosen.
        THe user can then bet from those match.
        """
        league_request_args = self.pages[2].args
        if  league_request_args != "":
            self.update_view(MatchPage(self))
            self.ids.bottom.remove_widget(self.submit)
            self.current_page += 1
        else:
            self.empty_args()

    def create_bets_page(self):
        """
        Create the page displaying all the bets made by the user
        The number chosen to declare the current page of this page
        was arbitrary and will be use every time we build a functionnality
        that has one page and is accessible from SportPage.
        """
        self.search = Search(self, BetPage)
        self.search.height = self.height / 15
        self.ids.pages.remove_widget(self.pages[0])
        self.pages.append(BetPage(self, None))
        self.ids.pages.add_widget(self.pages[1])
        self.ids.bottom.add_widget(self.backward)
        self.ids.search.add_widget(self.search)
        self.current_page = 9

    def create_winners_page(self):
        """
        Create the page displaying the 3 biggest winners from the app
        """
        self.ids.pages.remove_widget(self.pages[0])
        self.pages.append(BestPlayerPage())
        self.ids.pages.add_widget(self.pages[1])
        self.ids.bottom.add_widget(self.backward)
        self.current_page = 9

    def create_private_bets_page(self):
        """
        Create the page containing all the bets created by user.
        Anyone can then bet on any of those bets.
        """
        self.search = Search(self, PrivateBetPage)
        self.search.height = self.height / 15
        self.ids.pages.remove_widget(self.pages[0])
        self.pages.append(PrivateBetPage(self, None))
        self.ids.pages.add_widget(self.pages[1])
        self.ids.bottom.add_widget(self.backward)
        self.ids.search.add_widget(self.search)
        self.current_page = 9

    def update_view(self, page_to_add):
        """
        Method removing the widgets from the previous page to display the ones
        from the current page.
        """
        self.ids.pages.remove_widget(self.pages[self.current_page - 1])
        self.pages.append(page_to_add)
        self.ids.pages.add_widget(self.pages[self.current_page])
        if self.current_page == 1:
            self.ids.bottom.add_widget(self.submit)
            self.ids.bottom.add_widget(self.backward)

    def empty_args(self):
        """
        Raise a popup widget when the user doesn't chose any league or region
        and make a request.
        """
        pop = Popup(title='',
                    content=Label(text='Faites un choix'),
                    size_hint=(None, None), size=(self.width * 0.7, self.height * 0.4))
        pop.open()

        return pop

    def previous_view(self):
        """
        Method removing the actual widgets to display the ones from the
        previous page
        """
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
            self.ids.pages.add_widget(self.pages[0])
            self.current_page = 1
            if len(self.ids.search.children) == 1:
                self.ids.search.remove_widget(self.search)

    def logout(self):
        """
        Leave the betting screen to go on the login one
        """
        self.screenmanager.display.screens.pop()
        self.screenmanager.display.current = "login"

class Search(GridLayout):
    """
    Class creating and managing the search of specific widgets among ones returnd by
    a request
    """
    def __init__(self, player, object_to_search, **kwargs):
        super(Search, self).__init__(**kwargs)
        self.player = player
        self.object_to_search = object_to_search

    def update_private_bets(self):
        """
        It removes the page and create a new one adding  to itonly widgets containing
        infos specified in object_to_search.
        """
        self.player.ids.pages.remove_widget(self.player.pages[1])
        self.player.pages.pop()
        self.player.pages.append(self.object_to_search(self.player, self.ids.search_input.text))
        self.player.ids.pages.add_widget(self.player.pages[1])
