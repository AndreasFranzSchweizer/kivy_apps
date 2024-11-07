from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.event import EventDispatcher

class DataModel(EventDispatcher):
   title = StringProperty("")
   description = StringProperty("")

class MultiInputApp(App):
   def build(self):
      self.data_model = DataModel()

      main_layout = BoxLayout(orientation='vertical')

      main_layout.add_widget(Label(text='Title:'))
      text_input1 = TextInput(multiline=False)
      text_input1.bind(text=self.data_model.setter('title'))
      self.data_model.bind(title=text_input1.setter('text'))
      main_layout.add_widget(text_input1)

      main_layout.add_widget(Label(text='Description:'))
      text_input2 = TextInput(multiline=True)
      text_input2.bind(text=self.data_model.setter('description'))
      self.data_model.bind(description=text_input2.setter('text'))
      main_layout.add_widget(text_input2)

      main_layout.add_widget(Button(text='Print', on_press=self.print_values))
      
      return main_layout
   
   def print_values(self, instance):
      print('Title:', self.data_model.title)
      print('Description:', self.data_model.description)

if __name__ == '__main__':
   MultiInputApp().run()
