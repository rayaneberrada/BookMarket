import json

from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest

from screens.bet.bettingscreen import BettingScreen

Builder.load_file('screens/login/loginscreen.kv')

class LoginScreen(Screen):
    def __init__(self, screenmanager, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.screenmanager = screenmanager

    def login(self):
        username = self.ids.name.text.strip()
        password= self.ids.password.text.strip()
        if not username or not password:
            self.invalid_form()     
        else:
            params = json.dumps({"username": username, "password": password})
            headers = {"Content-Type": "application/json"}
            req = UrlRequest('http://127.0.0.1:5000/login', on_success=self.connected,
                on_failure=self.wrong_request, req_body=params, req_headers=headers)

    def connected(self, req, result):
        self.current_page = 0
        self.screenmanager.display.add_widget(BettingScreen(self.screenmanager ,result["user_id"], result["money"], name="bets"))
        self.ids.name.text = ""
        self.ids.password.text = ""
        self.screenmanager.display.current = "bets"

    def wrong_request(self, req, result):
        pop = Popup(title='Invalid Form',
                      content=Label(text=result["error_message"]),
                      size_hint=(None, None), size=(250, 250))

        pop.open()

    def register(self):
        self.ids.name.text = ""
        self.ids.password.text = ""
        self.screenmanager.display.current = "register"

    def invalid_form(self):
        pop = Popup(title='Invalid Form',
                      content=Label(text='Veuillez remplir tous les champs'),
                      size_hint=(None, None), size=(250, 250))

        pop.open()