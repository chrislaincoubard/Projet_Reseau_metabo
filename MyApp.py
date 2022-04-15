#code qui cree onglets et boutons, lors du clic un message est renvoyé dans le terminal

from ast import Return
from turtle import color
from webbrowser import BackgroundBrowser
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.config import Config
from kivy.uix.button import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.filechooser import FileChooserListView



class MyPanel(TabbedPanel):
    
    def call(self):
        print("CoucouLéLoulou")
        return



class MyApp(App):
    def build(self):
        return MyPanel()



if __name__ == '__main__':
	MyApp().run()



