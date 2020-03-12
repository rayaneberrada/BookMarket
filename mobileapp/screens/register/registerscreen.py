"""
File handling the logic of how the app work to register new users.
To manage the visual display of the registrering screen, check registeringscreen.kv.
"""
import json

from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest

class RegisterScreen(Screen):
    """
    Class displaying the screen to register new users.
    """
    def __init__(self, screenmanager, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.screenmanager = screenmanager

    def create_account(self):
        """
        This function get the informations from the inputs displayed in the screeen.
        If one of the input is empty, throw an error, otherwise, a request is sent
        to the server to save a new user with those informations.
        """
        username = self.ids.name.text.strip()
        password = self.ids.password.text.strip()
        if not username or not password:
            return self.popup_message('Veuillez remplir tous les champs')
        else:
            params = json.dumps({"username": username, "password": password})
            headers = {"Content-Type": "application/json"}
            return UrlRequest('http://206.189.118.233/register', on_success=self.display_message,
                              on_failure=self.display_message, on_error=self.display_message,
                              req_body=params, req_headers=headers)

    def display_message(self, req, result):
        """
        Function displaying the answer from the server.
        If the message indicate a success of the registering, the input entries are cleaned and
        the user is sent back on the login page.
        Otherwiser display an error message if returned by the server, or a connexion issue
        if the server couldn't be reached
        """
        if "succes_message" in result:
            self.login()
            return self.popup_message(result["succes_message"])
        elif "error_message" in result:
            return self.popup_message(result["error_message"])
        else:
            return self.popup_message("Connexion avec le serveur impossible")

    def popup_message(self, message):
        """
        Popup displayed to the user showing the message used in argument.
        """
        message = Popup(title="",
                        content=Label(text=message),
                        size_hint=(None, None), size=(self.width*0.7, self.height*0.4))
        message.open()
        return message.content.text
        #It returns text to help for testing

    def login(self):
        """
        In top of being called when creating a new user, this function is also called from the
        reigsterscreen.kv file when the user click on the text indicating he already has an account.
        It empty the inputs values and move the user to the login screen
        """
        self.ids.name.text = ""
        self.ids.password.text = ""
        self.screenmanager.display.current = "login"
