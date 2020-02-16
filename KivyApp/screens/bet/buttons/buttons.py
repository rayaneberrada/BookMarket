from kivy.lang.builder import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image  

Builder.load_file('screens/bet/buttons/buttons.kv')

class SubmitButton(ButtonBehavior, Image):
    def __init__(self, next_view, **kwargs):
        super(SubmitButton, self).__init__(**kwargs)
        self.next_view = next_view

    def on_press(self):
        self.next_view(None)

class GoBackward(ButtonBehavior, Image):
    def __init__(self, previous_view, **kwargs):
        super(GoBackward, self).__init__(**kwargs)
        self.previous_view = previous_view

    def on_press(self):
        self.previous_view()