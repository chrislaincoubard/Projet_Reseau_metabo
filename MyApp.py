from kivy.clock import Clock
from cgitb import text
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
import New_Graph
import subprocess
import os
Window.size=(1000,800)


class MyPanel(TabbedPanel):
    files={"gff":"","sbml":"","fna":"","tsv":"","faa1":"","faa2":"","json":""}
    select=False
    format=""
    buttonName=""
    clearFiles=False
    module="main"
    old_module=""
    parametre={"i":50,"d":30,"ev":10^100,"c":20,"bs":300}
    defaut={"i":50,"d":30,"ev":10^100,"c":20,"bs":300}
    filesName=""
    text_input = ObjectProperty(text)
    verifie_replace=False
    the_load_check=False
    graph = New_Graph.Graph("")
    
    def print_files(self):
        affiche=[]
        liste_blast=["faa1","faa2","gff","sbml"]
        liste_mpwting=["gff","fna","tsv"]
        liste_main=["faa1","faa2","gff","sbml","fna","tsv"]

        if self.module=="blast":
            for extension in liste_blast:
                name_files=self.files.get(extension).split("/")
                affiche.append([extension,name_files[-1]])       
            layout = GridLayout(cols=1,size_hint=(0.8,0.8))
            popupLabel = Label(text = f"{affiche[0][0]} : {affiche[0][1]}\n\n {affiche[1][0]} : {affiche[1][1]}\n \n {affiche[2][0]} : {affiche[2][1]} \n\n {affiche[3][0]} : {affiche[3][1]}",font_size='20sp')
            closeButton = Button(text = "Exit",color="#F00020")
            closeButton.bind(on_press=self.callback)
            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)       
            self._popup = Popup(title ='Files',size_hint =(0.8,0.8)) 
            self._popup.add_widget(layout) 
            self._popup.open()   
        
        elif self.module=="mpwting":
            for extension in liste_mpwting:
                name_files=self.files.get(extension).split("/")
                affiche.append([extension,name_files[-1]])    
            layout = GridLayout(cols=1,size_hint=(0.8,0.8))
            popupLabel = Label(text = f"{affiche[0][0]} : {affiche[0][1]}\n\n {affiche[1][0]} : {affiche[1][1]}\n \n {affiche[2][0]} : {affiche[2][1]}",font_size='20sp')
            closeButton = Button(text = "Exit",color="#F00020")
            closeButton.bind(on_press=self.callback)
            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)       
            self._popup = Popup(title ='Files',size_hint =(0.8,0.8)) 
            self._popup.add_widget(layout) 
            self._popup.open()   
            
        else:
            for extension in liste_main:
                name_files=self.files.get(extension).split("/")
                affiche.append([extension,name_files[-1]])        
            layout = GridLayout(cols=1,size_hint=(0.8,0.8))
            popupLabel = Label(text =f"{affiche[0][0]} : {affiche[0][1]}\n\n {affiche[1][0]} : {affiche[1][1]}\n\n {affiche[2][0]} : {affiche[2][1]}\n\n {affiche[3][0]} : {affiche[3][1]} \n\n {affiche[4][0]} : {affiche[4][1]}\n\n {affiche[5][0]} : {affiche[5][1]}",font_size='20sp')
            closeButton = Button(text = "Exit",color="#F00020")
            closeButton.bind(on_press=self.callback)
            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)       
            self._popup = Popup(title ='Files',size_hint =(0.8,0.8)) 
            self._popup.add_widget(layout) 
            self._popup.open()

    def callback(self,instance):
        if instance.state=="down":
            self.dismiss_popup()
            

    def dismiss_popup(self):
        self._popup.dismiss()

    def dismiss_popup_dt(self, dt):
        self._popup.dismiss()

    def show_load(self,textName,extension,textModule):
        self.buttonName=textName
        self.format=extension
        self.old_module=self.module
        self.module=textModule
        if self.module!=self.old_module:
            for key in self.files.keys():
                self.files[key] = ""


        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.the_load_check=False
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
        self.filesName=filename[0]
        verifie=self.check_format()
        if verifie or self.verifie_replace:
            self.dismiss_popup()
            self.verifie_replace=False
        extension = filename[0].split(".")
        if extension[1] == "json":
            self.graph.load_file(filename[0])
        
    def go_module(self):
        check_value=True
        if self.module=="blast" and self.files.get("faa1")!="" and self.files.get("faa2")!="" and self.files.get("gff")!="" and self.files.get("sbml")!="":
            if self.files.get("faa1")==self.files.get("faa2"):
                check_value=False
            if check_value:
                self.launch_blasting(self.files)
        if self.module=="mpwting" and self.files.get("tsv")!="" and self.files.get("fna")!="" and self.files.get("gff")!="":
            self.launch_mpwting(self.files)
        if self.module=="main" :
            for values in self.files.values():
                if values=="":
                    check_value=False
                if self.files.get("faa1")==self.files.get("faa2"):
                    check_value=False
            if check_value:
                self.launch_main(self.files)

    def check_format(self):
        good_format=False
        extension=self.filesName.split(".")
        if extension[1] == self.format:
            for key in self.files.keys():
                if key == self.buttonName :
                    if self.files.get(key)!="":
                        content = ChoiceFiles(cancel=self.dismiss_popup, test =ChoiceFiles.selectchoice)
                        self._popup = Popup(title="Replace files", content=content,size_hint=(0.4, 0.4))
                        self._popup.open()

                    else:
                        self.files[key]=self.filesName
                        good_format=True
                    
        else:
            self._popup = Popup(title='Error',content=Label(text='Wrong format, try again'),size_hint=(0.5,0.5))
            self._popup.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)
        return(good_format)
            
    def changefiles(self):
        self.files[self.buttonName]=self.filesName
        self.verifie_replace=True
    
    def launch_blasting(self,files):
        cmd = f"python3 blasting.py {files[0]} {files[1]} {files[2]} {files[3]}"
        p = subprocess.Popen(cmd, shell = True)
        p.wait()
        if p.returncode == 0 :
            print('command : success')
        else :
            print('command : fail')
        self.files.clear()
    
    def launch_mpwting(self,files):
            cmd = f"python3 mpwting.py {files[0]} {files[1]} {files[2]}"
            p = subprocess.Popen(cmd, shell = True)
            p.wait()
            if p.returncode == 0 :
                print('command : success')
            else :
                print('command : fail')
            self.files.clear()

    def launch_main(self,files):
        cmd = f"python3 blasting.py {files[0]} {files[1]} {files[2]} {files[3]} {files[4]} {files[5]} {files[6]}"
        p = subprocess.Popen(cmd, shell = True)
        p.wait()
        if p.returncode == 0 :
            print('command : success')
        else :
            print('command : fail')
        self.files.clear()


    def show_param(self):
        content = Parameters(cancel= self.dismiss_popup)
        self._popup = Popup(title="Enter Parameters", content=content,size_hint=(1,1))
        self._popup.open()

    def toggle_react_list(self):
        if self.ids["Reac_list"].opacity == 0:
            self.ids["Reac_list"].opacity = 1
        else:
            self.ids["Reac_list"].opacity = 0

    def clear_graph_data(self):
        self.graph.clear_data()

    def update_keyword(self, btn):
        self.ids["TI_Metab"].text = btn.text
        self.graph.meta_keyword_update(btn.text)

    def show_graph(self):
        self.graph.create_Graph(self.ids["TI_graph"].text)

    def save_graph(self):
        self.graph.save_graph_json(self.ids["TI_save"].text)
    
         
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class ChoiceFiles(FloatLayout):
    cancel = ObjectProperty(None)
    test = ObjectProperty(None)

    def selectchoice(self):
        MyPanel.changefiles()
    

class Parameters(BoxLayout):
    cancel = ObjectProperty(None)

    def add_value(self,param,id):
        MyPanel.param=param
        MyPanel.id=id
        valeur=self.ids[id].text
        try:
            if valeur!="":
                value=float(valeur)
                if param=="ev" and value<=1 and value>=0:
                    MyPanel.parametre['ev'] = value
                elif param=="i" and value<=100 and value>=0:
                    MyPanel.parametre['i'] = value
                elif param=="d" and value<=100 and value>=0:
                    MyPanel.parametre['d'] = value
                elif param=="c" and value<=100 and value>=0:
                    MyPanel.parametre['c'] = value
                elif param=="bs" and value<=1000 and value>=0:
                    MyPanel.parametre['bs'] = value
                else:
                    self._popup = Popup(title='Error',content=Label(text="The entered value is not within the range"),size_hint=(0.5,0.5))
                    self._popup.open()          
        except:
            self._popup = Popup(title='Error',content=Label(text="Value is not numeric "),size_hint=(0.5,0.5))
            self._popup.open() 
    def reset(self):
        MyPanel.parametre.update(MyPanel.defaut)

class TI_meta(TextInput):

    def on_text(self, instance, value):
        self.parent.ids["Meta_list"].data = [{"text" : meta["id"], "root_widget" : self.parent.ids["Meta_list"]}for meta in MyPanel.graph.data["metabolites"] if value.upper() in meta["id"].upper()]



class TI_reac(TextInput):
    def on_text(self, instance, value):
        self.parent.ids["Reac_list"].data = [{"text" : reac["id"], "root_widget" : self.parent.ids["Reac_list"]}for reac in MyPanel.graph.data["reactions"] if value.upper() in reac["id"].upper()]

class Box_reac(BoxLayout):
    def toggle_reac_list(self):
        if self.ids["Reac_list"].opacity == 0:
            self.ids["Reac_list"].opacity = 1
            if MyPanel.graph.data:
                self.ids["Reac_list"].data = [{"text" : meta["id"], "root_widget" : self.ids["Reac_list"]}for meta in MyPanel.graph.data["reactions"]]
        else :
            self.ids["Reac_list"].opacity = 0


class Box_meta(BoxLayout):

    def toggle_meta_list(self):
        if self.ids["Meta_list"].opacity == 0:
            self.ids["Meta_list"].opacity = 1
            if MyPanel.graph.data:
                self.ids["Meta_list"].data = [{"text" : meta["id"], "root_widget" : self.ids["Meta_list"]}for meta in MyPanel.graph.data["metabolites"]]
        else :
            self.ids["Meta_list"].opacity = 0



class Meta_list_buttons(Button):
    root_widget = ObjectProperty()

    def on_release(self, **kwargs):
        super().on_release()
        self.root_widget.btn_callback(self)


class Meta_List(RecycleView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if MyPanel.graph.data:
            self.data = [{"text" : meta["id"], 'root_widget' : self } for meta in MyPanel.graph.data["metabolites"]]

    def btn_callback(self, btn):
        self.parent.ids["TI_Metab"].text = btn.text
        MyPanel.graph.meta_keyword_update(btn.text)

class Reac_list_buttons(Button):
    root_widget = ObjectProperty()

    def on_release(self, **kwargs):
        super().on_release()
        self.root_widget.btn_callback(self)

class Reac_List(RecycleView):
    def __init__(self, **kwargs):
        super(Reac_List, self).__init__(**kwargs)
        if MyPanel.graph.data:
            self.data = [{"text" : reac["id"], 'root_widget' : self } for reac in MyPanel.graph.data["reactions"]]

    def btn_callback(self, btn):
        self.parent.ids["TI_reac"].text = btn.text
        MyPanel.graph.reac_keyword_update(btn.text)
        
class MyApp(App):
    
    def build(self):
        return MyPanel()
