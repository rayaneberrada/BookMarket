"""
This file test the code contained in loginscreen.py
"""
import pytest
from unittest.mock import Mock, patch

from kivy.lang.builder import Builder

from kivy.uix.screenmanager import ScreenManager
from screens.login.loginscreen import LoginScreen

Builder.load_file('tests/screens_test/loginscreen_test/loginscreen_test.kv')


class TestLoginScreen:
    """
    We instantiate the RegisterScreen class with a fake ScreenManager so that we can check it would
    supposely move to the login screen once the user is registered
    """
    FakeManager = Mock()
    object_to_test = LoginScreen(FakeManager)

    @pytest.mark.parametrize("username, password", [("", ""), ("Username", ""), ("", "Password")])
    def test_login_account_empty_credentials(self, username, password):
        """
        Check the app follow the right behavior when one or all inputs are empty
        """
        self.object_to_test.ids.name.text = username
        self.object_to_test.ids.password.text = password
        assert self.object_to_test.login() == "Veuillez remplir tous les champs"

    @patch('screens.login.loginscreen.UrlRequest')
    def test_login_account_with_credentials(self, mock_request):
        """
        Check that when the credentials exist, the UrlRequest is called
        """
        self.object_to_test.ids.name.text = "username"
        self.object_to_test.ids.password.text = "password"
        self.object_to_test.login()
        assert mock_request.called

    def test_connect(self):
        """
        Check that the connect function empty the inputs and move to the bets screen
        """
        request_result = {"user_id":1, "money":1000}
        self.object_to_test.connect(None, request_result)
        assert self.object_to_test.ids.name.text == ""
        assert self.object_to_test.ids.name.text == ""
        assert self.object_to_test.screenmanager.display.current == "bets"

    def test_register(self):
        """
        Check the app moves to the registering page and clean inputs entries when the user
        click on the text to ask for the registering page
        """
        self.object_to_test.register()
        assert self.object_to_test.ids.name.text == ""
        assert self.object_to_test.ids.password.text == ""
        assert self.object_to_test.screenmanager.display.current == "register"

    def test_cant_connect(self):
        """
        Check that when the request send back an error message, the right error message is displayed
        """
        assert self.object_to_test.cant_connect(None, {"error_message" : "La requête a échoué"}) == "La requête a échoué"

    def test_invalid_form(self):
        """
        Check when the user forget to fill all entries, the correct message is displayed.
        """
        assert self.object_to_test.invalid_form() == "Veuillez remplir tous les champs"