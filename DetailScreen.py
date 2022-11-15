import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.uix.textinput import TextInput

class DetailScreen(Screen):
    def on_enter(self):
        print(f'DetailScreen on_enter()')
        ### Get myname from the app object and update the top app bar
        app = MDApp.get_running_app()
        self.ids.toolbar.title = app.username
        print(app.screenmanager.current)
        ### Get the real-time database reference from the app
        db_ref = app.db_ref

        ### Get the selected item from the app
        key = app.selected_item

        ### Get data from the real-time through the database reference
        data = db_ref.child('ShoppingItem/details/' + key).get()
        if data != None:
            ### Show the data if the data is ready
            self.description = data['description']
            self.name = data['name']
            self.pictureURL = data['pictureURL']
            self.price = data['price']
            self.post_date, self.post_time = data['post_time'].split(',')
        else:
            ### Otherwise, you may show a message to inform the user about the problem
            pass

    def buy(self):
        number = self.ids.number.text
        try:
            number = int(number)
            app = MDApp.get_running_app()
            key = app.selected_item
            db_ref = app.db_ref
            data = db_ref.child('ShoppingItem/details/' + key).get()
            item = {'name': data['name'], 'pictureURL': data['pictureURL'], 'number': number, 'price': data['price']} 

            db_ref.child('ShoppingItem/cart').push(item)
            number = int(number)
            dialog = MDDialog(
                title = 'Add to cart',
                text = 'Successfully add '+ str(number) + ' item to cart!',
                buttons = [
                    MDRaisedButton(
                        text = 'OK', 
                        on_press = lambda x: dialog.dismiss()),
                ])
            dialog.open()
        except:
            dialog = MDDialog(
                title = 'Error',
                text = 'Invalid Input! Number should be a number!',
                buttons = [
                    MDRaisedButton(
                        text = 'OK', 
                        on_press = lambda x: dialog.dismiss()),
                ])
            dialog.open()

    def on_leave(self):
        self.ids.toolbar.title = ''
        self.price = ''
        self.name = ''
        self.description = ''
        self.post_time = ''
        self.post_date = ''
