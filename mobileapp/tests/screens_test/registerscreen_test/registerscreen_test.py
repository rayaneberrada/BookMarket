"""
This file test the code contained in registerscreen.py
"""
import pytest
from unittest.mock import Mock, patch

from kivy.lang.builder import Builder
from screens.register.registerscreen import RegisterScreen

Builder.load_file('tests/screens_test/registerscreen_test/registerscreen_test.kv')

class TestRegisterScreen:
    """
    We instantiate the RegisterScreen class with a fake ScreenManager so that we can check it would
    supposely move to the login screen once the user is registered
    """
    FakeManager = Mock()
    FakeManager.display.current = "register"
    object_to_test = RegisterScreen(FakeManager())

    def test_popup(self):
        """
        Check the pop widget contained the right message
        """
        popup_widget = self.object_to_test.popup_message("example")
        assert popup_widget == "example"

    def test_login(self):
        """
        Check the app moves to the login page and clean inputs entries once the user is registered
        """
        self.object_to_test.login()
        assert self.object_to_test.ids.name.text == ""
        assert self.object_to_test.ids.password.text == ""
        assert self.object_to_test.screenmanager.display.current == "login"

    @pytest.mark.parametrize("username, password", [("", ""), ("Username", ""), ("", "Password")])
    def test_create_account_empty_credentials(self, username, password):
        """
        Check the app follow the right behavior when one or all inputs are empty
        """
        self.object_to_test.ids.name.text = username
        self.object_to_test.ids.password.text = password
        assert self.object_to_test.create_account() == "Veuillez remplir tous les champs"

    @patch("screens.register.registerscreen.UrlRequest")
    def test_create_account_with_credentials(self, mock_request):
        """
        Check the app follow the right behavior when inputs contains informations
        """
        self.object_to_test.ids.name.text = "username"
        self.object_to_test.ids.password.text = "password"
        self.object_to_test.create_account()
        assert mock_request.called

    @pytest.mark.parametrize("request_answer, message",\
    [({"succes_message" : "Compte créé"}, "Compte créé"),\
    ({"error_message" : "Cet utilisateur existe déjà"}, "Cet utilisateur existe déjà")])
    def test_create_account_succeed(self, request_answer, message):
        """
        Check the callback of the UrlRequest display the expected message when called
        """
        assert self.object_to_test.display_message(None, request_answer) == message
