from io import BufferedRandom
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
import Graph
import subprocess
import os
Window.size=(1000,800)


class MyPanel(TabbedPanel):
    
    files={"gff":"","sbml":"","fna":"","tsv":"","faaM":"","faaS":"","json":""} #dictionary to store file names according to format
    format="" #takes the value of the extension expected by the clicked button
    buttonName="" #takes the value of the button id of the clicked button
    module="" #takes the value of the modulus of the clicked button
    old_module="" #takes the value of the modulus of the previous clicked button
    parametre={"i":50,"d":30,"ev":0,"c":20,"bs":300,"nom": "draft"} #dictionary to store values parameters of module
    defaut={"i":50,"d":30,"ev":0,"c":20,"bs":300,"nom": "draft"} #dictionary to store default values parameters of module
    filesName="" #take the path of the loaded file
    text_input = ObjectProperty(text)
    input=False
    mainDirectory="" #take the path of the main directory
    graph = Graph.Graph("")
    
            
    #close a pop-up
    def dismiss_popup(self):
        self._popup.dismiss()

    #close a pop-up after dt time
    def dismiss_popup_dt(self, dt):
        self._popup1.dismiss()

    #open the load dialog
    def show_load(self,textName,extension,textModule):
        self.buttonName=textName
        self.format=extension
        self.old_module=self.module
        self.module=textModule
        if self.module!=self.old_module: #delete files and restore settings if user changes module
            for key in self.files.keys():
                self.files[key] = ""
            self.parametre.update(self.defaut)
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup) #define the content of the pop-up
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    #get the path of the uploaded file 
    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
        self.filesName=filename[0]
        verifie=self.check_format()
        if verifie :
            self.dismiss_popup()
        extension = filename[0].split(".")
        if extension[1] == "json":
            self.graph.load_file(filename[0])

    """check if the extension of the uploaded file is the extension expected by the clicked button
    if the extension is the good , the path id added to the dictionnary files at the corresponding key,
    else the function alerts the user of his error.
    If a file already exists for the extension then it is replaced """
    def check_format(self):
        good_format=False
        extension=self.filesName.split(".")
        if extension[1] == self.format:
            for key in self.files.keys():
            
                if key == self.buttonName :
                    if self.files.get(key)!="":
                        self._popup1 = Popup(title="Replace files", content=Label(text="Updated File"),size_hint=(0.4, 0.4))
                        self._popup1.open()
                        Clock.schedule_once(self.dismiss_popup_dt, 2)
                        self.files[key]=self.filesName
                        good_format=True
                    else:
                        self.files[key]=self.filesName
                        self._popup1 = Popup(title="Replace files", content=Label(text="File successfully loaded ..."),size_hint=(0.4, 0.4))
                        self._popup1.open()
                        Clock.schedule_once(self.dismiss_popup_dt, 2)
                        self.files[key]=self.filesName
                        good_format=True
                    
        else:
            self._popup1 = Popup(title='Error',content=Label(text='Wrong format, try again'),size_hint=(0.5,0.5))
            self._popup1.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)
        return (good_format)

    def choosedirectory(self):
        self._popup=Popup(title="Choose  a main directory", content = DirectoryName(cancel=self.dismiss_popup),size_hint=(0.5,0.5))
        self._popup.open()
    
    def temp_dir(self):
        os.mkdir("temp_dir")
        for key in self.files.keys():
            os.system(f"cp {self.files[key]} temp_dir")


    """ check if the main directory exists and if the all necessary files are downloaded for the module.
    if is true , the module is run , else the function alerts the user of his error"""
    def go_module(self):
        check_value=True
        if self.module=="blast" or self.module=="main":
            if  self.mainDirectory=="":
                check_value=False
                self._popup1 = Popup(title='Error',content=Label(text='Please enter a main directoryt'),size_hint=(0.5,0.5))
                self._popup1.open()
                Clock.schedule_once(self.dismiss_popup_dt, 1)
        
        if self.module=="blast" :
            if self.files.get("faaS")!="" and self.files.get("faaM")!="" and self.files.get("gff")!="" and self.files.get("sbml")!="":
                if self.files.get("faaS")==self.files.get("faaM"):
                    check_value=False
                    self._popup1 = Popup(title='Error',content=Label(text='Fasta files must be different'),size_hint=(0.5,0.5))
                    self._popup1.open()
                    Clock.schedule_once(self.dismiss_popup_dt, 1)
            
            else:
                self._popup1 = Popup(title='Error',content=Label(text='Please load all necessary files'),size_hint=(0.5,0.5))
                self._popup1.open()
                Clock.schedule_once(self.dismiss_popup_dt, 1)
                check_value=False
            if check_value:
                self.launch_module()
        if self.module=="mpwting":
            if self.files.get("tsv")!="" and self.files.get("fna")!="" and self.files.get("gff")!="":
                self.launch_module()
            else:
                self._popup1 = Popup(title='Error',content=Label(text='Please load all necessary files'),size_hint=(0.5,0.5))
                self._popup1.open()
                Clock.schedule_once(self.dismiss_popup_dt, 1)
        if self.module=="main":
            if self.files.get("faaS")!="" and self.files.get("faaM")!="" and self.files.get("gff")!="" and self.files.get("sbml")!="" and self.files.get("fna")!="" and self.files.get("tsv")!="":
                
                if self.files.get("faaM")==self.files.get("faaS"):
                    self._popup1 = Popup(title='Error',content=Label(text='Fasta files must be different'),size_hint=(0.5,0.5))
                    self._popup1.open()
                    Clock.schedule_once(self.dismiss_popup_dt, 1)
                    check_value=False
            else:
                self._popup1 = Popup(title='Error',content=Label(text='Please load all necessary files'),size_hint=(0.5,0.5))
                self._popup1.open()
                Clock.schedule_once(self.dismiss_popup_dt, 1)
                check_value=False
            
            if check_value:
                self.launch_module()
            
              

    def launch_module(self):
        if self.module == "blast":
            cmd = f"python3 blasting.py {self.mainDirectory} -n {self.parametre['nom']} -m {self.files['sbml']} -mfaa {self.files['faaM']} -sfaa {self.files['faaS']} -sgff {self.files['gff']} -i {self.parametre['i']} -d {self.parametre['d']} -ev {self.parametre['ev']} -c {self.parametre['c']} -bs {self.parametre['bs']}"
        if self.module == "mpwting":
            cmd = f"python3 "
        if self.module == "main":
            self.temp_dir()
            cmd = f"python3 main.py {self.mainDirectory} -m {self.files['sbml']} -mfaa {self.files['faaM']} -sfaa {self.files['faaS']} -sgff {self.files['gff']} -i {self.parametre['i']} -d {self.parametre['d']} -ev {self.parametre['ev']} -c {self.parametre['c']} -bs {self.parametre['bs']} "
        p = subprocess.Popen(cmd, shell = True)
        p.wait()
        os.system("rm -rf ./temp_dir/")
        if p.returncode == 0 :
            print('command : success')
        else :
            print('command : fail')
        self.files.clear()

    #informs the user of the files already downloaded
    def print_files(self):
        affiche=[]
        liste_blast=["faaM","faaS","gff","sbml"] #list of the necessary files for blast module
        liste_mpwting=["gff","fna","tsv"] #list of the necessary files for mpwt module
        liste_main=["faaM","faaS","gff","sbml","fna","tsv"] #list of the necessary files for main module

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
            self.input=True

    #open the settings dialog
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
        
    def print_keyword(self):
        layout = GridLayout(cols=1, size_hint=(0.8, 0.8))
        popupLabel = Label(
            text=f"current metabolites searched : {self.graph.meta_keyword}\n current reactions searched : {self.graph.reac_keyword}",
            font_size='20sp')
        closeButton = Button(text="Exit", color="#F00020")
        closeButton.bind(on_press=self.callback)
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)
        self._popup = Popup(title='Files', size_hint=(0.8, 0.8))
        self._popup.add_widget(layout)
        self._popup.open()

#define the object load dialog        
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

#define the object choice folder dialog
class DirectoryName(BoxLayout):
    cancel = ObjectProperty(None)
    
    def add_directory(self,inputname):
        valeur=self.ids[inputname].text
        if valeur != "":
            MyPanel.mainDirectory= valeur
            
#define the object settings dialog
class Parameters(BoxLayout):
    cancel = ObjectProperty(None)

    """check if the value in textinput is in the interval, if is true the value of the dictionnary parameter is replace,
    else the function alerts the user of his error"""
    def add_value(self,param,id):
        
        valeur=self.ids[id].text
        
        if id == "input6":
            MyPanel.parametre[param] = value
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
            
   # replace the value in parameter with default values
    def reset(self):
        MyPanel.parametre.update(MyPanel.defaut)

class TI_meta(TextInput):

    def on_text(self, instance, value):
        if self.parent.ids["Meta_list"].data :
            self.parent.ids["Meta_list"].data = [{"text" : meta["id"], "root_widget" : self.parent.ids["Meta_list"]}for meta in MyPanel.graph.data["metabolites"] if value.upper() in meta["id"].upper()]



class TI_reac(TextInput):
    def on_text(self, instance, value):
        if self.parent.ids["Reac_list"].data :
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
        if self.opacity == 1:
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
        if self.opacity == 1:
            self.parent.ids["TI_reac"].text = btn.text
            MyPanel.graph.reac_keyword_update(btn.text)
        
class MyApp(App):
    
    def build(self):
        return MyPanel()