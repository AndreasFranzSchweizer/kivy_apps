from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.event import EventDispatcher

# Datenmodell mit zwei Properties für die Eingabewerte
class DataModel(EventDispatcher):
   value1 = StringProperty("")
   value2 = StringProperty("")

class MultiInputApp(App):
   def build(self):
      # Initialisierung des Datenmodells
      self.data_model = DataModel()

      # Layout für die UI
      main_layout = BoxLayout(orientation='vertical')

      text_input1 = TextInput(multiline=False)
      text_input2 = TextInput(multiline=False)

      text_input1.bind(text=self.data_model.setter('value1'))
      self.data_model.bind(value1=text_input1.setter('text'))
      text_input2.bind(text=self.data_model.setter('value2'))
      self.data_model.bind(value2=text_input2.setter('text'))

      main_layout.add_widget(text_input1)
      main_layout.add_widget(text_input2)
      main_layout.add_widget(Button(text='Print', on_press=self.print_values))
      
      return main_layout
   
   def print_values(self, instance):
      print('Value1:', self.data_model.value1)
      print('Value2:', self.data_model.value2)

if __name__ == '__main__':
   MultiInputApp().run()
