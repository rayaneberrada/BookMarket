"""
File handling the logic of how the app work to login new users.
To manage the visual display of the login screen, check loginscreen.kv.
"""
import json

from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest

from screens.bet.bettingscreen import BettingScreen

class LoginScreen(Screen):
    """
    This class manage the connection of the user to the app.
    """
    def __init__(self, screenmanager, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.screenmanager = screenmanager

    def login(self):
        """
        If username and password entries are not empty, the function request necessery informations
        to instantiate the BettingScreen class that will display functionnalities and available
        sports from which we can check the odds and bet on.
        """
        username = self.ids.name.text.strip()
        password = self.ids.password.text.strip()
        if not username or not password:
            return invalid_form()

        params = json.dumps({"username": username, "password": password})
        headers = {"Content-Type": "application/json"}
        return UrlRequest('http://127.0.0.1:5000/login', on_success=self.connect,
                          on_failure=wrong_request, req_body=params, req_headers=headers)

    def connect(self, req, result):
        """
        If UrlRequest send back a succes code, this method is called and BettingScreen instantiated
        with informations sent by the server.
        The object is then added to the ScreenManager class and the current screen display move to
        this one.
        """
        self.screenmanager.display.add_widget(BettingScreen\
            (self.screenmanager, result["user_id"], result["money"], name="bets"))
        self.ids.name.text = ""
        self.ids.password.text = ""
        self.screenmanager.display.current = "bets"

    def register(self):
        """
        Function called when the user wants to move on the registering screen
        """
        self.ids.name.text = ""
        self.ids.password.text = ""
        self.screenmanager.display.current = "register"

def wrong_request(req, result):
    """
    If UrlRequest send back a failure code, a popup appears with the reason of the failure
    """
    message = Popup(title='Invalid Form',
                    content=Label(text=result["error_message"]),
                    size_hint=(None, None), size=(250, 250))
    message.open()
    return message.content.text

def invalid_form():
    """
    Method called when one or all of the inputs of the login screen are empty
    """
    message = Popup(title='Invalid Form',
                    content=Label(text='Veuillez remplir tous les champs'),
                    size_hint=(None, None), size=(250, 250))
    message.open()

    return message.content.text
