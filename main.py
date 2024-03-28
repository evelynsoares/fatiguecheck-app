from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
import math
import matplotlib.pyplot as plt

class SplashArt(Screen):
    pass
    
class FirstWindow(Screen):
   # cable_type_str = StringProperty()
   # def on_text_validate(self, widget):
    #    self.cable_type_str = widget.text
    def clear_text(self):
        self.diameter.text = ""

class SecondWindow(Screen):
    pass

class ThirdWindow(Screen):
    pass

class FourthdWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass



class testsApp(App):
    pass

testsApp().run()