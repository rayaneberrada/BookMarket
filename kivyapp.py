from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior 
from kivy.uix.image import Image  
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
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
import functools
from kivy.uix.popup import Popup
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout


class PageManager(Screen):
    PAGE = 0
    REQUEST_REGION = ""
    REQUEST_MATCHES = ""
    def __init__(self, **kwargs):
        super(PageManager, self).__init__(**kwargs)
        self.sport_page = None
        self.region_page = None
        self.league_page = None
        self.match_page = None
        self.submit = None
        self.backward = None
        self.create_view(None)

    def create_view(self, choice):
        if PageManager.PAGE == 0:
            self.sport_page = SportPage(self.create_view)
            self.ids.pages.add_widget(self.sport_page)
            PageManager.PAGE += 1
        elif PageManager.PAGE == 1:
            self.ids.pages.remove_widget(self.sport_page)
            self.region_page = RegionPage(choice)
            self.submit = SubmitButton(self.create_view)
            self.backward = GoBackward(self.previous_view)
            self.ids.pages.add_widget(self.region_page)
            self.ids.bottom.add_widget(self.submit)
            self.ids.bottom.add_widget(self.backward)
            PageManager.PAGE += 1
        elif PageManager.PAGE == 2 and self.REQUEST_REGION != "":
            self.ids.pages.remove_widget(self.region_page)
            self.league_page = LeaguePage()
            self.ids.pages.add_widget(self.league_page)
            PageManager.PAGE += 1
        elif PageManager.PAGE == 2 and self.REQUEST_REGION == "":
            pop = Popup(title='Invalid Request',
                  content=Label(text='Choisissez au moins une région'),
                  size_hint=(None, None), size=(400, 400))
            pop.open()
        elif PageManager.PAGE == 3 and self.REQUEST_MATCHES != "":
            self.ids.pages.remove_widget(self.league_page)
            self.ids.bottom.remove_widget(self.submit)
            match_manager = MatchPage()
            self.match_page = match_manager.create_grid_matches()
            self.ids.pages.add_widget(self.match_page)
            PageManager.PAGE += 1
        elif PageManager.PAGE == 3 and self.REQUEST_MATCHES == "":
            pop = Popup(title='Invalid Request',
                  content=Label(text='Choisissez au moins un championnat'),
                  size_hint=(None, None), size=(400, 400))
            pop.open()

    def previous_view(self):
        if PageManager.PAGE == 2:
            self.ids.pages.remove_widget(self.region_page)
            self.ids.bottom.remove_widget(self.submit)
            self.ids.bottom.remove_widget(self.backward)
            self.ids.pages.add_widget(self.sport_page)
            PageManager.PAGE -= 1
        elif PageManager.PAGE == 3:
            self.ids.pages.remove_widget(self.league_page)
            self.ids.pages.add_widget(self.region_page)
            PageManager.PAGE -= 1
        elif PageManager.PAGE == 4:
            self.ids.pages.remove_widget(self.match_page)
            self.ids.pages.add_widget(self.league_page)
            self.ids.bottom.add_widget(self.submit)
            PageManager.PAGE -= 1
            # popup error window
        #----------------------------------------------
        #attributes used to navigate in the application

        #----------------------------------------------
        """
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
    


    def create_match_display(self, infos):
        match = GridLayout(cols=1, size_hint_y=None, height=Window.height*(3/5))
        first_row = " ".join([ x for x in [infos["date"], " ", infos["tv"]] if x is not None])
        match.add_widget(Label(text=first_row))
        second_row = GridLayout(cols=3)
        second_row.add_widget(Label(text=str(infos["cote_dom"])))
        second_row.add_widget(Label(text=str(infos["domicile"])))
        second_row.add_widget(Label(text="RING"))
        match.add_widget(second_row)
        third_row = GridLayout(cols=3)
        third_row.add_widget(Label(text=str(infos["cote_nul"])))
        third_row.add_widget(Label(text="Nul"))
        third_row.add_widget(Label(text="RING"))
        match.add_widget(third_row)
        forth_row = GridLayout(cols=3)
        forth_row.add_widget(Label(text=str(infos["cote_ext"])))
        forth_row.add_widget(Label(text=str(infos["exterieur"])))
        forth_row.add_widget(Label(text="RING"))
        match.add_widget(forth_row)
        self.scrollinfos.add_widget(match)

            
    """
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if PageManager.PAGE == 2:
            arg_to_add = "region=" + urllib.parse.quote(rv.data[index]["text"])
            if is_selected:
                PageManager.REQUEST_REGION += arg_to_add + "&"
                print(PageManager.REQUEST_REGION)

            else:
                args = PageManager.REQUEST_REGION.split("&")
                for arg in args:
                    if arg_to_add == arg:
                        args.remove(arg)
                PageManager.REQUEST_REGION = "&".join(args)
        elif PageManager.PAGE == 3:
            arg_to_add = "competition=" + urllib.parse.quote(rv.data[index]["text"])
            if is_selected:
                PageManager.REQUEST_MATCHES += arg_to_add + "&"
                print(PageManager.REQUEST_MATCHES)

            else:
                args = PageManager.REQUEST_MATCHES.split("&")
                for arg in args:
                    if arg_to_add == arg:
                        args.remove(arg)
                PageManager.REQUEST_MATCHES = "&".join(args)

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

class Match(GridLayout):
    pass

class MatchPage(GridLayout):
    def __init__(self,**kwargs):
        super(MatchPage, self).__init__(**kwargs)
        self.cols = 1
        self.gridlayout = GridLayout(cols=1, size_hint_y=None,  spacing=10)
        self.gridlayout.bind(minimum_height=self.gridlayout.setter('height'))
        
    def add_to_view(self, req, result):
        for value in result["matches"]:
            match = Match()
            match.ids.title.text = value["date"]
            match.ids.bet_home.text = value["cote_dom"] + " " + value["domicile"]
            match.ids.bet_draw.text = value["cote_dom"] + " Nul"
            match.ids.bet_away.text = value["cote_ext"] + " " + value["exterieur"]
            self.gridlayout.add_widget(match)

    def create_grid_matches(self):
        print(PageManager.REQUEST_MATCHES)
        requestMatches = UrlRequest('http://127.0.0.1:5000/rencontres?' + PageManager.REQUEST_MATCHES, self.add_to_view)
        return self.gridlayout

class LeaguePage(RecycleView):
    def __init__(self, **kwargs):
        super(LeaguePage, self).__init__(**kwargs)
        self.data = []
        requestLeagues = UrlRequest("http://127.0.0.1:5000/rencontres/competitions?" + PageManager.REQUEST_REGION, self.parse_json)

    def parse_json(self, req, result):
        self.data = []
        for value in result["competitions"]:
            self.data.append({"text" : value})

class RegionPage(RecycleView):
    def __init__(self, arg, **kwargs):
        super(RegionPage, self).__init__(**kwargs)
        self.data = []
        PageManager.REQUEST_REGION = ""
        requestRegions = UrlRequest('http://127.0.0.1:5000/rencontres/{}/regions'.format(arg), self.parse_json)

    def parse_json(self, req, result):
        self.data = []
        for value in result["regions"]:
            self.data.append({"text": value, "on_press": functools.partial(self.add_arg_to_request, value)})
            self.url_request_regions = req.url

    def add_arg_to_request(self, req_arg):
        #print(self.view_adapter.get_visible_view(5))
        arg_to_search = "region="
        """
        elif self.PAGE == 3:
            arg_to_search = "competition="
        """

        req_arg = urllib.parse.quote(req_arg) 
        if req_arg in PageManager.REQUEST_REGION:
            args = PageManager.REQUEST_REGION.split("&")
            for arg in args:
                if req_arg in arg:
                    args.remove(arg)
            PageManager.REQUEST_REGION = "&".join(args)
        else:
            if PageManager.REQUEST_REGION:
                PageManager.REQUEST_REGION += "&" + arg_to_search + req_arg
            else:
                PageManager.REQUEST_REGION += arg_to_search + req_arg
        print(PageManager.REQUEST_REGION)


class SportPage(RecycleView):
    def __init__(self, next_view, **kwargs):
        super(SportPage, self).__init__(**kwargs)
        self.data = []
        self.next_view = next_view
        self.request_json(None)

    def request_json(self, arg):
        requestCompetition = UrlRequest('http://127.0.0.1:5000/sports', self.parse_json)

    def parse_json(self, req, result):
        self.data = []
        for value in result["sports"]:
            self.data.append({"text" : value['nom'], "on_press" : functools.partial(self.next_view, value['nom'])})
            self.url_request_sport = req.url

class BookMarket(App):
    def build(self):
        return PageManager()
 
BookMarket().run()