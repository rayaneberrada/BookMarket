import json

from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest

Builder.load_file('screens/register/registerscreen.kv')

class RegisterScreen(Screen):
    def __init__(self, screenmanager, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.screenmanager = screenmanager

    def create_account(self):
        username = self.ids.name.text.strip()
        password= self.ids.password.text.strip()
        if not username or not password:
            self.invalid_form()
        else:
            params = json.dumps({"username": username, "password": password})
            headers = {"Content-Type": "application/json"}
            req = UrlRequest('http://127.0.0.1:5000/users', on_success=self.display_message,
                on_failure=self.display_message, req_body=params, req_headers=headers)

    def display_message(self, req, result):
        if "succes_message" in result:
            self.request_answer(result["succes_message"])
            self.screenmanager.display.current = "login"
        elif "error_message" in result:
            self.request_answer(result["error_message"])

    def login(self):
        self.ids.name.text = ""
        self.ids.password.text = ""
        self.screenmanager.display.current = "login"

    def invalid_form(self):
        pop = Popup(title='Invalid Form',
                      content=Label(text='Veuillez remplir tous les champs'),
                      size_hint=(None, None), size=(250, 250))

        pop.open()

    def request_answer(self, message):
        pop = Popup(title='Invalid Form',
                      content=Label(text=message),
                      size_hint=(None, None), size=(250, 250))

        pop.open()