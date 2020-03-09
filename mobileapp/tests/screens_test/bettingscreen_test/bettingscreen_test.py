"""
This file test the code contained in screens/bet/bettingscreen.py
"""
from unittest.mock import patch

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from screens.bet.bettingscreen import BettingScreen
from  screens.bet.pages.bestplayers.bestplayerspage import BestPlayerPage
from  screens.bet.pages.bet.betpage import BetPage
from  screens.bet.pages.match.matchpage import MatchPage
from  screens.bet.pages.matchselection.selectionpages import SportPage, RegionPage, LeaguePage
from  screens.bet.buttons.buttons import GoBackward, SubmitButton

Builder.load_file('tests/screens_test/bettingscreen_test/bettingscreen_test.kv')

class FakeScreen:
    """
    Class containing the reference to the fake current screen displayed by the kivy app
    """
    current = "register"
    screens = [1, 2, 3]

class FakeManager(ScreenManager):
    """
    Class managing the fake screen
    """
    display = FakeScreen()

class TestBettingScreen:
    """
    This class contain all the necessary test to check all the methods from
    BettingScreen are following the right behavior.
    """
    object_to_test = BettingScreen(FakeManager(), "fake_user", 1000)

    def test_create_bets_page(self):
        """
        Check BetPage is correctly created and added to our display
        """
        self.object_to_test.current_page = 1
        self.object_to_test.create_bets_page()
        assert self.object_to_test.current_page == 9
        assert isinstance(self.object_to_test.ids.pages.children[0], BetPage)
        assert isinstance(self.object_to_test.ids.bottom.children[0], GoBackward)

    def test_bets_previous_view(self):
        """
        Check we get back on the SportPage with the right widgets when using the
        previous_view method from the BetPage object
        """
        self.object_to_test.previous_view()
        assert self.object_to_test.current_page == 1
        assert isinstance(self.object_to_test.ids.pages.children[0], SportPage)
        assert not isinstance(self.object_to_test.ids.bottom.children[0], GoBackward)
        assert not isinstance(self.object_to_test.ids.bottom.children[1], SubmitButton)

    def test_create_winners_page(self):
        """
        Check BestPlayerPage is correctly created and added to our display
        """
        self.object_to_test.current_page = 1
        self.object_to_test.create_winners_page()
        assert self.object_to_test.current_page == 9
        assert isinstance(self.object_to_test.ids.pages.children[0], BestPlayerPage)
        assert isinstance(self.object_to_test.ids.bottom.children[0], GoBackward)

    def test_winners_previous_view(self):
        """
        Check we get back on the SportPage with the right widgets when using the
        previous_view method from the BestPlayerPage object
        """
        self.object_to_test.previous_view()
        assert self.object_to_test.current_page == 1
        assert isinstance(self.object_to_test.ids.pages.children[0], SportPage)
        assert not isinstance(self.object_to_test.ids.bottom.children[0], GoBackward)
        assert not isinstance(self.object_to_test.ids.bottom.children[1], SubmitButton)

    def test_sport_page(self):
        """
        Sport page is created when we initialize the class so we don't need to
        call the function creating it.
        We then jsut need to check the method behaved as expected.
        """
        assert len(self.object_to_test.pages) == 1
        assert self.object_to_test.current_page == 1
        assert isinstance(self.object_to_test.ids.pages.children[0], SportPage)

    def test_region_page(self):
        """
        Check RegionPage object and the related widgets to make it works are
        correctly added to our display.
        """
        self.object_to_test.current_page = 1
        self.object_to_test.create_region_page()
        assert len(self.object_to_test.pages) == 2
        assert self.object_to_test.current_page == 2
        assert isinstance(self.object_to_test.ids.pages.children[0], RegionPage)
        assert isinstance(self.object_to_test.ids.bottom.children[0], GoBackward)
        assert isinstance(self.object_to_test.ids.bottom.children[1], SubmitButton)

    def test_region_page_previous_view(self):
        """
        Check we display the SportPage and remove the rights widgets when we use
        previous_view from the RegionPage page.
        """
        self.object_to_test.previous_view()
        assert len(self.object_to_test.pages) == 1
        assert self.object_to_test.current_page == 1
        assert isinstance(self.object_to_test.ids.pages.children[0], SportPage)
        assert not isinstance(self.object_to_test.ids.bottom.children[0], GoBackward)
        assert not isinstance(self.object_to_test.ids.bottom.children[1], SubmitButton)

    @patch('screens.bet.bettingscreen.BettingScreen.empty_args')
    def test_league_page_fail(self, mock_empty_args):
        """
        Check empty_args method is called when the user user create_league_page without
        having selected any regions to search for before submitting the request.
        """
        self.object_to_test.create_region_page()
        self.object_to_test.pages[1].args = ""
        self.object_to_test.create_league_page()
        assert mock_empty_args.called

    def test_create_league_page_succes(self):
        """
        Check LeaguePage object is correctly replacing RegionPage and the necessary
        widgets are still present
        """
        self.object_to_test.pages[1].args = "args_exist"
        self.object_to_test.current_page = 2
        self.object_to_test.create_league_page()
        assert len(self.object_to_test.pages) == 3
        assert self.object_to_test.current_page == 3
        assert isinstance(self.object_to_test.ids.pages.children[0], LeaguePage)

    def test_create_league_page_previous_view(self):
        """
        Verify that RegionPage page replace LeaguePage page when called from LeaguePage.
        """
        self.object_to_test.previous_view()
        assert len(self.object_to_test.pages) == 2
        assert self.object_to_test.current_page == 2
        assert isinstance(self.object_to_test.ids.pages.children[0], RegionPage)
        assert isinstance(self.object_to_test.ids.bottom.children[0], GoBackward)
        assert isinstance(self.object_to_test.ids.bottom.children[1], SubmitButton)

    def test_create_match_page_succes(self):
        """
        Check MatchPage page is correctly replacing LeaguePage page and the correct
        widgets are removed
        """
        self.object_to_test.create_league_page()
        self.object_to_test.pages[2].args = "args_exist"
        self.object_to_test.current_page = 3
        self.object_to_test.create_match_page()
        assert len(self.object_to_test.pages) == 4
        assert self.object_to_test.current_page == 4
        assert isinstance(self.object_to_test.ids.pages.children[0], MatchPage)

    def test_create_match_page_previous_view(self):
        """
        Check LeaguePage page is replacing MatchPage page when previous_view is called
        from the last one.
        """
        self.object_to_test.previous_view()
        assert len(self.object_to_test.pages) == 3
        assert self.object_to_test.current_page == 3
        assert isinstance(self.object_to_test.ids.pages.children[0], LeaguePage)
        assert isinstance(self.object_to_test.ids.bottom.children[0], SubmitButton)
        assert isinstance(self.object_to_test.ids.bottom.children[1], GoBackward)

    @patch('screens.bet.bettingscreen.BettingScreen.empty_args')
    def test_match_page_fail(self, mock_empty_args):
        """
        Check empty_args is called when create_match_page is called without any
        arguments present in LeaguePage.args
        """
        self.object_to_test.pages[2].args = ""
        self.object_to_test.create_match_page()
        assert mock_empty_args.called

    @patch('screens.bet.bettingscreen.BettingScreen.create_match_page')
    @patch('screens.bet.bettingscreen.BettingScreen.create_league_page')
    @patch('screens.bet.bettingscreen.BettingScreen.create_region_page')
    @patch('screens.bet.bettingscreen.BettingScreen.create_sport_page')
    def test_create_view(self, mock_sport, mock_region, mock_league, mock_match):
        """
        Check that for each possible value of current_page the right method is called
        """
        self.object_to_test.current_page = 0
        self.object_to_test.create_view(None)
        assert mock_sport.called
        self.object_to_test.current_page = 1
        self.object_to_test.create_view(None)
        assert mock_region.called
        self.object_to_test.current_page = 2
        self.object_to_test.create_view(None)
        assert mock_league.called
        self.object_to_test.current_page = 3
        self.object_to_test.create_view(None)
        assert mock_match.called

    def test_empty_args(self):
        """
        Check empty_args return the right output
        """
        assert self.object_to_test.empty_args().content.text == 'Saisissez une réponse'

    def test_update_money(self):
        """
        Check update_money modify properly the amount variable
        """
        self.object_to_test.update_money()
        assert self.object_to_test.ids.amount.text == "Solde: 1000"

    def test_logout(self):
        """
        Check that when the logout is called, the user is sent on the right screen
        and the functionnalities widget is destroyed
        """
        self.object_to_test.logout()
        assert len(self.object_to_test.screenmanager.display.screens) == 2
        assert self.object_to_test.screenmanager.display.current == "login"
