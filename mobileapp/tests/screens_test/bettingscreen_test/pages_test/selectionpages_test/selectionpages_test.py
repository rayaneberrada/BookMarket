"""
File checking screens.bet.pages.matchselection.selectionpage.py always keep the
right behavior
"""
from unittest.mock import patch
from unittest.mock import Mock

from screens.bet.bettingscreen import BettingScreen
from  screens.bet.pages.matchselection.selectionpages import SportPage, RegionPage, LeaguePage

class TestSportPage:
    """
    Check that SportPage methods follow the right behavior
    """
    object_to_test = SportPage(BettingScreen)

    @patch("kivy.network.urlrequest.UrlRequest")
    def test_request(self, request_mock):
        """
        Check that a request is sent and that the method parse the code in
        the expected way
        """
        response = {
            "sports":[{"nom":"Football"},
                      {"nom":"Rugby"}]
        }
        request_mock.return_value = self.object_to_test.parse_json(None, response)
        assert len(self.object_to_test.data) == 5
        assert self.object_to_test.data[0]["text"] == "Football"
        assert self.object_to_test.data[2]["text"] == "Paris privés"
        assert self.object_to_test.data[3]["text"] == "Historique paris"
        assert self.object_to_test.data[4]["text"] == "Plus gros gagnants"

class TestRegionPage:
    """
    Check that RegionPage methods follow the right behavior
    """
    object_to_test = RegionPage(BettingScreen, "Football")

    @patch("kivy.network.urlrequest.UrlRequest")
    def test_request(self, request_mock):
        """
        Check that a request is sent and that the method parse the code in
        the expected way
        """
        response = {
            "regions":["France", "Allemagne", "Espagne"]
        }
        request_mock.return_value = self.object_to_test.parse_json(None, response)
        assert len(self.object_to_test.data) == 3
        assert self.object_to_test.data[0]["text"] == "France"

class TestLeaguePage:
    """
    Check that LeaguePage methods follow the right behavior
    """
    fakeBettingScreen = Mock()
    fakeBettingScreen.return_value = "Football"
    object_to_test = LeaguePage(fakeBettingScreen, "Region=France")

    @patch("kivy.network.urlrequest.UrlRequest")
    def test_request(self, request_mock):
        """
        Check that a request is sent and that the method parse the code in
        the expected way
        """
        response = {
            "competitions":["Ligue 1", "Ligue 2"]
        }
        request_mock.return_value = self.object_to_test.parse_json(None, response)
        assert len(self.object_to_test.data) == 2
        assert self.object_to_test.data[0]["text"] == "Ligue 1"
