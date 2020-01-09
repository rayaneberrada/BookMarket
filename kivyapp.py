from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.app import App
from functools import partial
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import urllib.parse
from pprint import pprint

class Screen(GridLayout):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        #----------------------------------------------
        #attributes used to navigate in the application
        self.current_page = 0
        self.url_request_sport = None
        self.url_request_regions = None
        self.url_request_leagues = None
        self.request_arguments = ""
        #----------------------------------------------
        self.cols = 1 # Set columns for main layout
        self.tittle = Button(text="BookMarket", font_size=40, size_hint_y=None, height=Window.height/5)
        self.add_widget(self.tittle)
        self.request_json(None)

        #-------------------------------------------------
    def backward(self, button):
        if self.current_page == 2:
            self.clean_interface()
            self.create_grid_for_json_datas()
            self.current_page -= 2
            requestCompetition = UrlRequest(self.url_request_sport, self.parse_json)
            
        elif self.current_page == 3:
            self.clean_interface()
            self.create_grid_for_json_datas()
            self.current_page -= 2
            requestCompetition = UrlRequest(self.url_request_regions, self.parse_json)
            
        elif self.current_page == 4:
            self.clean_interface()
            self.create_grid_for_json_datas()
            self.current_page -= 2
            requestCompetition = UrlRequest(self.url_request_leagues, self.parse_json)
            

    def add_to_matches_request(self, button):
        print(self.current_page)
        if self.current_page == 2:
            arg_to_search = "region="
        elif self.current_page == 3:
            arg_to_search = "competition="
        if button.text in self.request_arguments:
            args = self.request_arguments.split("&")
            for arg in args:
                if button.text in arg:
                    args.remove(arg)
            self.request_arguments = "&".join(args)
        else:
            if self.request_arguments:
                self.request_arguments += "&" + arg_to_search + urllib.parse.quote(button.text)
            else:
                self.request_arguments += arg_to_search + urllib.parse.quote(button.text)
        print(self.request_arguments)

    def create_submit_buttons(self):
        self.add_widget(self.inside)
        if self.current_page == 0:
            self.bottom_grid = Button(text="Submit", font_size=40,size_hint_y=None, height=Window.height/5)
            self.add_widget(self.bottom_grid) # Add the button to the main layout 4
        elif self.current_page >= 1:
            self.bottom_grid = GridLayout(cols=3, size_hint_y=None, height=Window.height/5)
            self.back_button = Button(text="Backward", font_size=40)
            self.back_button.bind(on_press=self.backward)
            self.submit = Button(text="Submit", font_size=40)
            self.submit.bind(on_press=self.request_json)
            self.favorite = Button(text="Favorites")
            self.bottom_grid.add_widget(self.back_button)
            self.bottom_grid.add_widget(self.submit)
            self.bottom_grid.add_widget(self.favorite)
            self.add_widget(self.bottom_grid) # Add the button to the main layout 4
         # Add the interior layout to the main
        #--------------------------------------------------
    
    def clean_interface(self):
        self.remove_widget(self.inside)
        self.remove_widget(self.bottom_grid)

    def create_grid_for_json_datas(self):
        self.inside = GridLayout(size_hint_y=None, height=(Window.height)*(3/5)) # Create a new grid layout
        self.inside.cols = 3 # set columns for the new grid layout
        self.inside.add_widget(Widget())
        # height=int(Window.height)/8.9

        self.informations = ScrollView(size_hint=(1, None), height=(Window.height)*(3/5))
        self.scrollinfos = (GridLayout(cols=1, spacing=0, size_hint_y=None))
        self.scrollinfos.bind(minimum_height=self.scrollinfos.setter('height'))
        self.informations.add_widget(self.scrollinfos)
    
    def parse_json(self, req, result):
        switcher = {
                    0:"sports",
                    1:"regions",
                    2:"competitions",
                    3:"matches"
        }
        data_searched = switcher.get(self.current_page)
        for value in result[data_searched]:
            if data_searched == "sports":
                self.button = Button(text="{}".format(value['nom']), size_hint_y=None, height=Window.height/10)
                self.button.bind(on_press=self.request_json)
                self.scrollinfos.add_widget(self.button)
                self.url_request_sport = req.url
            elif data_searched == "regions":
                self.button = ToggleButton(text="{}".format(value), size_hint_y=None, height=Window.height/10)
                self.button.bind(on_press=self.add_to_matches_request)
                self.scrollinfos.add_widget(self.button)
                self.url_request_regions = req.url
            elif data_searched == "competitions":
                print(value)
                self.button = ToggleButton(text="{}".format(value), size_hint_y=None, height=Window.height/10)
                self.button.bind(on_press=self.add_to_matches_request)
                self.scrollinfos.add_widget(self.button)
                self.request_arguments = ""
                self.url_request_leagues = req.url
            elif data_searched == "matches":
                self.create_match_display(value)

        self.inside.add_widget(self.informations)
        self.inside.add_widget(Widget())
        self.create_submit_buttons()
        self.current_page += 1

    def create_match_display(self, infos):
        self.match = GridLayout(cols=1, size_hint_y=None, height=Window.height*(3/5))
        self.first_row = " ".join([ x for x in [infos["date"], " ", infos["tv"]] if x is not None])
        self.match.add_widget(Label(text=self.first_row))
        self.second_row = GridLayout(cols=3)
        self.second_row.add_widget(Label(text=str(infos["cote_dom"])))
        self.second_row.add_widget(Label(text=str(infos["domicile"])))
        self.second_row.add_widget(Label(text="RING"))
        self.match.add_widget(self.second_row)
        self.third_row = GridLayout(cols=3)
        self.third_row.add_widget(Label(text=str(infos["cote_nul"])))
        self.third_row.add_widget(Label(text="Nul"))
        self.third_row.add_widget(Label(text="RING"))
        self.match.add_widget(self.third_row)
        self.forth_row = GridLayout(cols=3)
        self.forth_row.add_widget(Label(text=str(infos["cote_ext"])))
        self.forth_row.add_widget(Label(text=str(infos["exterieur"])))
        self.forth_row.add_widget(Label(text="RING"))
        self.match.add_widget(self.forth_row)
        self.scrollinfos.add_widget(self.match)

            

    def request_json(self, button_infos):
        if self.current_page == 0:
            self.create_grid_for_json_datas()
            requestCompetition = UrlRequest('http://127.0.0.1:5000/sports', self.parse_json)
        elif self.current_page == 1:
            self.clean_interface()
            self.create_grid_for_json_datas()
            requestRegions = UrlRequest('http://127.0.0.1:5000/rencontres/{}/regions'.format(button_infos.text), self.parse_json)
        elif self.current_page == 2:
            self.clean_interface()
            self.create_grid_for_json_datas()
            print(self.request_arguments)
            requestLeagues = UrlRequest("http://127.0.0.1:5000/rencontres/competitions?" + self.request_arguments, self.parse_json)
        elif self.current_page == 3:
            self.clean_interface()
            self.create_grid_for_json_datas()
            requestMatches = UrlRequest('http://127.0.0.1:5000/rencontres?' + self.request_arguments, self.parse_json)



class KivyButton(App):

 
    def disable(self, instance, *args):
 
        instance.disabled = True
 
    def update(self, instance, *args):
 
        instance.text = "I am Disabled!"
 
    def build(self):
        
 
        mybtn = Button(text="Click me to disable")
 
        mybtn.bind(on_press=partial(self.disable, mybtn))
 
        mybtn.bind(on_press=partial(self.update, mybtn))
 
        return Screen()
 
KivyButton().run()