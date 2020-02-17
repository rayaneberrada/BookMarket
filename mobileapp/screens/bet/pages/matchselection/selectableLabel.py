import urllib.parse

from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior

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
        if rv.screen.current_page == 2:
            arg_to_add = "region=" + urllib.parse.quote(rv.data[index]["text"])
            if is_selected and arg_to_add not in rv.args:
                rv.args += arg_to_add + "&"
                print(rv.args)
            elif is_selected and arg_to_add in rv.args:
                pass
            elif not is_selected:
                args = rv.args.split("&")
                for arg in args:
                    if arg_to_add == arg:
                        args.remove(arg)
                rv.args = "&".join(args)
        elif rv.screen.current_page == 3:
            arg_to_add = "competition=" + urllib.parse.quote(rv.data[index]["text"])
            if is_selected and arg_to_add not in rv.args:
                rv.args += arg_to_add + "&"
                print(rv.args)
            elif is_selected and arg_to_add in rv.args:
                pass
            else:
                args = rv.args.split("&")
                for arg in args:
                    if arg_to_add == arg:
                        args.remove(arg)
                rv.args = "&".join(args)