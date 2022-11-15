### the following three lines are used for SSL problem on some computers.
### do NOT forget to add the following three lines to your code if you want to download something from the Internet
import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
import json

from mandel_layouts import SwipeItem
class MyCartItem(SwipeItem):
    def delete(self):
        app = MDApp.get_running_app()
        db_ref = app.db_ref
        db_ref.child('ShoppingItem/cart/' + self.id).delete()
        print(f'DELETE: {self.id}')
        self.dismiss()

    def dosomething(self):
        print('CLICK:')
        print(self.title)
        print(self.content)
        print(self.id)

class CartScreen(Screen):
    
    def on_enter(self):

        app = MDApp.get_running_app()
        self.ids.toolbar.title = 'Shopping cart'
        ### find the container widget, reset it, and scroll to the top
        container = self.ids.container
        container.clear_widgets()

    
        db_ref = app.db_ref

        ### open a JSON file in readonly mode and read all lines
        data = db_ref.child('ShoppingItem/cart').get()
        
        ### find the container and delete the existing items
        container = self.ids.container
        container.clear_widgets()

        ### add items to the container
        if(data != None):   
            for k in data.keys():
                d = data[k]
                item = MyCartItem()
                item.title = d['name']
                item.count = 'x' + str(d['number'])
                item.price = 'Total price: ' + str(int(d['price']) * int(d['number']))
                item.pictureURL = d['pictureURL']
                item.id = k
                container.add_widget(item)
                container.ids[k] = item
