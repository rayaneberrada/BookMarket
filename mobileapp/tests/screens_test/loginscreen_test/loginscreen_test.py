"""
This file test the code contained in registerscreen.py
"""
import pytest

from kivy.lang.builder import Builder

from kivy.uix.screenmanager import ScreenManager
from screens.login.loginscreen import LoginScreen, wrong_request, invalid_form

Builder.load_file('tests/screens_test/loginscreen_test/loginscreen_test.kv')

class FakeBettingScreen(ScreenManager):
    """
    Class containing the reference to the fake current screen displayed by the kivy app
    """
    current = "login"

class FakeManager(ScreenManager):
    """
    Class managing the fake screen
    """
    display = FakeBettingScreen

class TestLoginScreen:
    """
    We instantiate the RegisterScreen class with a fake ScreenManager so that we can check it would
    supposely move to the login screen once the user is registered
    """
    object_to_test = LoginScreen(FakeManager())

    @pytest.mark.parametrize("username, password", [("", ""), ("Username", ""), ("", "Password")])
    def test_login_account_empty_credentials(self, username, password):
        """
        Check the app follow the right behavior when one or all inputs are empty
        """
        self.object_to_test.ids.name.text = username
        self.object_to_test.ids.password.text = password
        assert self.object_to_test.login() == "Veuillez remplir tous les champs"

    def test_login_account_with_credentials(self):
        self.object_to_test.ids.name.text = "username"
        self.object_to_test.ids.password.text = "password"
        assert self.object_to_test.login().url == 'http://206.189.118.233/login'

    def test_connect(self, monkeypatch):
        def mock_connect():
            self.object_to_test.ids.name.text = ""
            self.object_to_test.ids.password.text = ""
            self.object_to_test.screenmanager.display.current = "bets"

        self.object_to_test.connect = mock_connect
        self.object_to_test.connect()
        assert self.object_to_test.ids.name.text == ""
        assert self.object_to_test.ids.name.text == ""
        assert self.object_to_test.screenmanager.display.current == "bets"

    def test_register(self):
        """
        Check the app moves to the login page and clean inputs entry once the user is registered
        """
        self.object_to_test.register()
        assert self.object_to_test.ids.name.text == ""
        assert self.object_to_test.ids.password.text == ""
        assert self.object_to_test.screenmanager.display.current == "register"

def test_wrong_request():
    """
    Check that when the request send back an error message, it is correctly process
    """
    assert wrong_request(None, {"error_message" : "La requête a échoué"}) == "La requête a échoué"

def test_invalid_form():
    """
    Check when the user forget to fill all entries, the correct message is displayed.
    """
    assert invalid_form() == "Veuillez remplir tous les champs"