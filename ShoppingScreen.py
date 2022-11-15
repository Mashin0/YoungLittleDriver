### the following three lines are used for SSL problem on some computers.
### do NOT forget to add the following three lines to your code if you want to download something from the Internet
import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()

from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp

from mandel_layouts import ListItem

class ShoppingItem(ListItem):
    def show_details(self):
        key = self.key
        print(f'You clicked the item with key {key}')

        app = MDApp.get_running_app()
        # app.last_screens.append(app.screenmanager.current)
        # print(app.screenmanager.current)

        ### remember which item is selected
        app.selected_item = key
        print(app.selected_item)
    
        ### show the another screen to show the content
        app.show_screen('DetailScreen')

class ShoppingScreen(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        self.ids.toolbar.title = app.username
        ### find the container widget, reset it, and scroll to the top
        container = self.ids.container
        container.clear_widgets()
        container.parent.scroll_y = 1
    
        db_ref = app.db_ref

        # data = db_ref.child('messages/titles').get()
        data = db_ref.child('ShoppingItem/details').get()

        if data != None:
            for key in data.keys():

                ### get a record from the resulted data using the key
                value = data[key]

                ### Create a new ShoppingItem widget for the record
                item = ShoppingItem()

                ### Store the key, it will be useful for further actions, such as update, delete, or so on
                item.key = key

                ### Put the info to the ShoppingItem widget
                item.title = value['name']
                item.post_date, item.post_time = value['post_time'].split(',')
                item.pictureURL = value['pictureURL']
                item.price = value['price']

                ### Add the widget to the container
                container.add_widget(item)

        else:
            ### If there are no records
            self.empty()

    def empty(self):
        ### add a label to the container
        container = self.ids.container
        container.height = container.parent.height
        label = MDLabel()
        label.text = 'Empty'
        label.halign = 'center'
        container.add_widget(label)

    def on_leave(self):
        self.ids.toolbar.title = ''

