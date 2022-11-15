from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

class HomeScreen(Screen):
    def on_enter(self):
        ### Get myname from the app object and update the top app bar
        app = MDApp.get_running_app()
        self.ids.toolbar.title = app.username

    def on_leave(self):
        self.ids.toolbar.title = ''
