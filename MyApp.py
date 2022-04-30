
from kivy.clock import Clock
from cgitb import text
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from functools import partial

import subprocess
import os



class MyPanel(TabbedPanel):
    files={"gff":"","sbml":"","fna":"","tsv":"","faa1":"","faa2":""}
    select=False
    format=""

    nomBouton=""
    clearFiles=False
    module="blast"
    ancien_module=""
    parametre={"i":50,"d":30,"ev":10^100,"c":20,"bs":300}
    defaut={"i":50,"d":30,"ev":10^100,"c":20,"bs":300}
    
    text_input = ObjectProperty(text)
    

    def print_ids(self):
        print(self.ids)
    

    def print_files(self):
        print(self.files)
    

    def dismiss_popup(self):
        self._popup.dismiss()

    def dismiss_popup_dt(self, dt):
        self._popup.dismiss()

    def show_load(self,text,extension,textbis):
        self.nomBouton=text
        self.format=extension
        self.ancien_module=self.module
        self.module=textbis
        if self.module!=self.ancien_module:
            for key in self.files.keys():
                self.files[key] = ""


        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()



    def load(self, path, filename):
        
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
        
        self.check_format(filename)
        
        
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
        

         

    def check_format(self, filename):
        extension=filename.split(".")
        if extension[1] == self.format:
            for key in self.files.keys():
                if self.files[key] == self.nomBouton :
                    if self.files.get(key)!="":
                        content = ChoiceFiles(cancel=self.dismiss_popup, test =ChoiceFiles.selectchoice)
                        self._popup = Popup(title="Replace files", content=content,size_hint=(0.4, 0.4))
                        self._popup.open()
                    else:    
                        self.files[key]=filename
                    if self.select==True:
                        self.files[key]=filename
                    
        else:
            self._popup = Popup(title='Erreur',content=Label(text='Mauvais Format,reesayez'),size_hint=(0.5,0.5))
            self._popup.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)
        self.select=False
            

   
        


    
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
    
    


    def show_clear(self):
        content = Choice(cancel=self.dismiss_popup, test = Choice.clear_files)
        self._popup = Popup(title="Clear file", content=content,
                            size_hint=(0.4, 0.4))
        self._popup.open()



    def show_param(self):
        content = Parametres(cancel= self.dismiss_popup)
        self._popup = Popup(title="Enter Parameters", content=content,
                            size_hint=(1,1))
        self._popup.open()
    
    
    


    
        
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Choice(FloatLayout):
    cancel = ObjectProperty(None)
    test = ObjectProperty(None)
    
    def clear_files(self):
        for key in MyPanel.files.keys():
            MyPanel.files[key] = ""
        self._popup = Popup(title='Informations',content=Label(text='Liste de fichiers effacée'),size_hint=(0.5,0.5))
        self._popup.open()

class ChoiceFiles(FloatLayout):
    cancel = ObjectProperty(None)
    test = ObjectProperty(None)

    def selectchoice(self):
        MyPanel.select=True
    
    
        
        
    

class Parametres(BoxLayout):
    
    cancel = ObjectProperty(None)
    def add_value(self,param,id):
        
        valeur=self.ids[id].text
        print(valeur)
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
                self._popup = Popup(title='Erreur',content=Label(text="La valeur entrée n'est pas comprise dans l'intervalle "),size_hint=(0.5,0.5))
                self._popup.open()

    def reset(self):
        MyPanel.parametre.update(MyPanel.defaut)
            
        
        
class MyApp(App):
    
    def build(self):
       
        return MyPanel()
    

if __name__ == '__main__':
	MyApp().run()
   

  