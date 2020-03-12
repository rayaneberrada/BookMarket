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
            return self.invalid_form()

        params = json.dumps({"username": username, "password": password})
        headers = {"Content-Type": "application/json"}
        return UrlRequest('http://206.189.118.233/login', on_success=self.connect,
                          on_failure=self.cant_connect, req_body=params, on_error=self.cant_connect,
                          req_headers=headers)

    def connect(self, req, result):
        """
        If UrlRequest send back a succes code, this method is called and BettingScreen instantiated
        with informations returned by the API.
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
        Function called when the user wants to move on the registering screen.
        """
        self.ids.name.text = ""
        self.ids.password.text = ""
        self.screenmanager.display.current = "register"

    def cant_connect(self, req, result):
        """
        If UrlRequest send back a failure code on an error, a popup appears with the reason of the failure
        """
        if "error_message" in result:
            message = Popup(title='',
                            content=Label(text=result["error_message"]),
                            size_hint=(None, None), size=(self.width * 0.7, self.height * 0.4))
        else:
            message = Popup(title='',
                            content=Label(text="Connexion indisponible"),
                            size_hint=(None, None), size=(self.width * 0.7, self.height * 0.4))

        message.open()
        return message.content.text

    def invalid_form(self):
        """
        Method called when one or all of the inputs of the login screen are empty
        """
        message = Popup(title='',
                        content=Label(text='Veuillez remplir tous les champs'),
                        size_hint=(None, None), size=(self.width * 0.7, self.height * 0.4))
        message.open()
        return message.content.text
