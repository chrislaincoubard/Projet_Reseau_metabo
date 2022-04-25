from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label



class TI(TextInput):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('widget touched')
            app = App.get_running_app()
            app.dropdown.open(self)
        return super().on_touch_down(touch)


class Test(App):

    def build(self):
        box = GridLayout(cols=3, rows=3)
        label = Label(text='LABEL1')
        label2 = Label(text='LABEL2')
        label3 = Label(text='LABEL3'

)
        ti = TI(text='Selection', font_size=30, size_hint_y=0.15)
        # self.ti.bind(on_touch_down=self.list_open)
        # self.ti.bind(on_touch_up= self.test_collide_list)
        box.add_widget(label)
        box.add_widget(label2)
        box.add_widget(label3)
        box.add_widget(ti)

        self.dropdown = DropDown()  # Create the dropdown once and keep a reference to it
        self.dropdown.bind(on_select=lambda instance, x: setattr(ti, 'text', x))
        # self.dropdown.text="drop"

        for index in range(10):  # create the buttons once
            btn = Button(text='Value %d' % index, size_hint_y=None, height=44,
                         on_release=lambda btn: print(btn.text))  # bind every btn to a print statement
            btn.text = 'Value %d' % index
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        return box

    # def list_open(self, button, *args):
    #     print("--------",button, args)
    #
    #
    #     self.dropdown.open(button)  # you need this to open the dropdown


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