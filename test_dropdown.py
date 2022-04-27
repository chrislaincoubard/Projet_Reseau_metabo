from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import New_Graph
from functools import partial



class TI(TextInput):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('widget touched')
            app = App.get_running_app()
            app.dropdown.open(self)
        return super().on_touch_down(touch)

    # def on_text(self,value):
    #     print(f"The widget, {self}, has a value of {value}" )
        # self.dropdown.clear_widgets()
        # for meta in self.graph.data["metabolites"]:
        #     if self.ti.text in meta["id"]:
        #         btn = Button(text=meta["id"], size_hint_y=None, height=44,
        #                      on_release=lambda btn: print(btn.text))  # bind every btn to a print statement
        #         btn.text = meta["id"]
        #         btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
        #         self.dropdown.add_widget(btn)

class Test(App):


    def calc(self, instance, text):
        print(text)
        # self.dropdown.clear_widgets()
        # for meta in self.graph.data["metabolites"]:
        #     if self.ti.text in meta["id"]:
        #         btn = Button(text=meta["id"], size_hint_y=None, height=44,
        #                      on_release=lambda btn: print(btn.text))  # bind every btn to a print statement
        #         btn.text = meta["id"]
        #         btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
        #         self.dropdown.add_widget(btn)

    def print_data(self,graph):
        print(f"keyword {graph.meta_keyword}, Meta {graph.Metabolites}, Reac {graph.Reaction}, nodes_M {graph.nodes_metabolites}, nodes_R {graph.nodes_reactions}")

    def build(self):
        graph = New_Graph.Graph("actinidia_chinensis_merged.json")
        box = GridLayout(cols=3, rows=3)
        label1 = Label(text = "Label 1")
        label1.size_hint=(0.3,0.3)
        label2 = Label(text='LABEL2')
        label2.size_hint=(0.3,0.3)
        label3 = Label(text='LABEL3')
        label3.size_hint=(0.3,0.3)
        btn = Button(text = 'PRINT THE_LIST', center_x = 0.5, center_y = 0.5)
        btn2 = TextInput(text = 'Show Graph', multiline=False)
        btn3 = Button(text = "New Graph" )



        ti = TI(text='', font_size=30, size_hint_y=0.15, multiline=False)
        ti.bind(on_text_validate = lambda ti: print(ti.text))
        ti.bind(text= self.calc)

        btn.bind(on_release= lambda btn: self.print_data(graph))
        btn.size_hint=(0.3,0.3)
        btn2.size_hint=(0.3,0.3)
        btn3.size_hint=(0.3,0.3)
        btn2.bind(on_text_validate=lambda btn2: graph.create_Graph(btn2.text))
        btn3.bind(on_release = lambda btn3: graph.clear_data())
        box.add_widget(label1)
        box.add_widget(label2)
        box.add_widget(label3)
        box.add_widget(btn)
        box.add_widget(btn2)
        box.add_widget(btn3)
        box.add_widget(ti)

        self.dropdown = DropDown()  # Create the dropdown once and keep a reference to it
        self.dropdown.bind(on_select=lambda instance, x: setattr(ti, 'text', x))

        for meta in graph.data["metabolites"]:  # create the buttons once
            btn = Button(text=meta["id"], size_hint_y=None, height=44,
                         on_release=lambda btn: print(btn.text))  # bind every btn to a print statement
            btn.text = meta["id"]
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text), on_press=lambda btn :graph.meta_keyword_update(btn.text))
            self.dropdown.add_widget(btn)
        return box



    def test_collide_list(self,*args):
        print("INST ")
        print("point ",*args[1].pos)
        for x in args:
            print("test", x)
        for w in self.dropdown.walk():
            print("Button" in str(w), *args[1].pos, w.collide_point(*args[1].pos), w.pos)
            if "Button" in str(w) and w.collide_point(*args[1].pos):
                print(w.text)

Test().run()