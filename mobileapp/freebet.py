"""
This file import the login screen and the registering one and launch the kivy application.
The user can then login or register.
The screen displaying the functionnalities is instantiated and added to the class inheriting
from ScreenManager(WindowManager) when the user connect.It happens inside the loginscreen.py file.
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

import freebet_kv
from screens.login.loginscreen import LoginScreen
from screens.register.registerscreen import RegisterScreen


class WindowManager(ScreenManager):
    """Class managing which screen view is displayed for the user"""

class FreeBet(App):
    """
    This class instantiate necessary objects to allow the user
    to register and connect. Once run, the kivy app will be launched.
    """
    def __init__(self, **kwargs):
        super(FreeBet, self).__init__(**kwargs)
        self.display = WindowManager()

    def build(self):
        screens = [LoginScreen(self, name="login"), RegisterScreen(self, name="register")]
        for screen in screens:
            self.display.add_widget(screen)
        self.display.current = "login"
        return self.display

if __name__ == "__main__":
    FreeBet().run()
