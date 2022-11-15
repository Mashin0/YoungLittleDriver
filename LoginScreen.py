### the following three lines are used for SSL problem on some computers.
### do NOT forget to add the following three lines to your code if you want to download something from the Internet
import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()

from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivy.app import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

import firebase_admin
from firebase_admin import db

from HomeScreen import HomeScreen
from ShoppingScreen import ShoppingScreen
from DetailScreen import DetailScreen
from CartScreen import CartScreen

### You need to download your own service account key file and store it together with your PY files
cred_obj = firebase_admin.credentials.Certificate('22407944.json')

### Check the database URL and storage URL from your Firebase console
### Replace the databaseURL and storageBucket with your owns
firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://comp7510-63ac4-default-rtdb.firebaseio.com/',
    'storageBucket':'comp7510-63ac4.appspot.com'
	})

class LoginScreen(Screen):
    def on_enter(self):
        ### Reset the text field
        self.ids.txt_username.text = ""
        self.ids.txt_password.text = ""

    def login(self):
        if self.ids.txt_username.text=='' or self.ids.txt_password.text=='':
            dialog = MDDialog(
            title = 'Error',
            text = 'Please enter all infomation',
            buttons = [
                MDRaisedButton(
                    text = 'OK', 
                    on_press = lambda x: dialog.dismiss()),
            ])
            dialog.open()
        else:
            username = self.ids.txt_username.text
            password = self.ids.txt_password.text
            print(f'Username: {username}.')
            print(f'password: {password}.')
            app = MDApp.get_running_app()
            app.show_screen('HomeScreen')
        
    def set_name(self):
        ### Update the value of myname defined in the app object
        app = MDApp.get_running_app()
        app.username = self.ids.txt_username.text.strip()

### If this file is not the starting file of the application, the following code will be ignored.
if __name__ == '__main__':
    from kivy.core.window import Window
    from kivy.utils import platform

    ### Set window size if the app runs on Windows or MacOS
    if platform in ('win', 'macosx'):
        Window.size = (500, 600)

    class MyApp(MDApp):
        screenmanager = None
        last_screens = []
        db_ref = db.reference('/')

        ### myname will be used by other screens too
        username = None

        def show_screen(self, screen_name):
            ### remember the last screen            
            self.last_screens.append(self.screenmanager.current)
            print(self.last_screens)
            self.screenmanager.add_widget(DetailScreen(name='DetailScreen'))


            ### set transition effect
            self.screenmanager.transition.direction = 'left'            

            ### change screen
            self.screenmanager.current = screen_name

        def go_back(self):
            ### get the name of the last screen
            screen_name = self.last_screens.pop()
            print(self.last_screens)

            ### set transition effect
            self.screenmanager.transition.direction = 'right'

            ### change screen
            self.screenmanager.current = screen_name

        ### The app starts with a screen. The screen defination is loaded from the KV file
        def build(self):
            self.title = ''
            Builder.load_file('LoginScreen.kv')
            Builder.load_file('ShoppingScreen.kv')
            Builder.load_file('DetailScreen.kv')
            Builder.load_file('HomeScreen.kv')
            Builder.load_file('CartScreen.kv')

            self.screenmanager = ScreenManager()

            self.screenmanager.add_widget(LoginScreen(name='LoginScreen'))
            self.screenmanager.add_widget(ShoppingScreen(name='ShoppingScreen'))
            self.screenmanager.add_widget(DetailScreen(name='DetailScreen'))
            self.screenmanager.add_widget(HomeScreen(name='HomeScreen'))
            self.screenmanager.add_widget(CartScreen(name='CartScreen'))

            return self.screenmanager

    MyApp().run()