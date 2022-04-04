from turtle import color
from webbrowser import BackgroundBrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.config import Config
from kivy.uix.button import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang import Builder


class Test(BoxLayout):
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)

        self.tabbedPanel = TabbedPanel(do_default_tab=False)

        #Définition du panneau à placer sur le panneau à onglets

        self.panel1 = TabbedPanelItem(text="Main")
        self.panel1.add_widget(Label(text="This is Panel 1"))

        #Définition du panneau à placer sur le panneau à onglets
        self.panel2 = TabbedPanelItem(text="BLAST")
        self.panel2.add_widget(
            Label(text="Veuillez choisir trois fichiers:",
                  color="#ff3333",
                  size_hint=(1.0, 0.1)))
        #button2=Button(text="Choose file", font_size="20sp",size_hint=(0.2 , 0.1),background_color="#FC0D0D",pos_hint={"center_x":0.5 , "center_y":0.9})
        button3 = Button(text="Choose file",
                         font_size="20sp",
                         size_hint=(0.2, 0.1),
                         background_color="#FC0D0D",
                         pos_hint={
                             "center_x": 0.9,
                             "center_y": 0.3
                         })

        self.panel2.add_widget(Button(text="Choose file", font_size="10sp"))
        self.panel2.add_widget(Button(text="Choose file", font_size="10sp"))
        self.panel2.add_widget(button3)

        #Définition du panneau à placer sur le panneau à onglets
        self.panel3 = TabbedPanelItem(text="MPWTing")
        self.panel3.add_widget(Label(text="This is Panel 2"))

        #Placer sur le panneau à onglets
        self.tabbedPanel.add_widget(self.panel1)
        self.tabbedPanel.add_widget(self.panel2)
        self.tabbedPanel.add_widget(self.panel3)

        #Mettre sur l'application
        self.add_widget(self.tabbedPanel)


class Sample(App):
    def build(self):
        return Test()


Sample().run()


# RPOBLEME BOUTON QUI BOUGE  PAS
