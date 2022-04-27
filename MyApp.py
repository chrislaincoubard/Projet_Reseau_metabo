
from kivy.uix.button import Button
from kivy.clock import Clock
from cgitb import text
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
import subprocess
import os

from numpy import empty


class MyPanel(TabbedPanel):
    files=[]
    format=""
    module="blast"
    ancien_module=""
    compteur_fasta=0
    compteur_sbml=0
    text_input = ObjectProperty(text)

    def dismiss_popup(self):
        self._popup.dismiss()

    def dismiss_popup_dt(self, dt):
        self._popup.dismiss()

    def show_load(self,text,textbis):
        self.format=text
        self.ancien_module=self.module
        self.module=textbis
        if self.module!=self.ancien_module:
            self.files.clear()
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, path, filename):
        
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        
        self.check_format(filename,self.files,self.format)
        print(self.files)
        if self.module=="blast" and len(self.files)==4:
            self.launch_blasting(self.files)
        if self.module=="mpwting" and len(self.files)==3:
            self.launch_mpwting(self.files)
        if self.module=="main" and len(self.files)==6:
            self.launch_main(self.files)
        
            

         

    def check_format(self, filename,files,format):
        the_format=True
        check = filename[0][-4:]
        compteur=0
        print(check)
        name=""
        if len(files) > 0 :
            for i in files:
                if i[-4:]==".faa":
                    compteur+=1
                    name=i
                    print("ici")
                if i[-4:]==format and i[-4:]!=".faa":
                    self.dismiss_popup()
                    self._popup = Popup(title='Erreur',content=Label(text='Format deja chargé,reessayez'),size_hint=(0.5,0.5))
                    self._popup.open()
                    Clock.schedule_once(self.dismiss_popup_dt, 1)
                    the_format=False
                    print("la")
                if format == ".faa" and compteur>=2:
                    self.dismiss_popup()
                    self._popup = Popup(title='Erreur',content=Label(text='Format deja chargé,reessayez'),size_hint=(0.5,0.5))
                    self._popup.open()
                    Clock.schedule_once(self.dismiss_popup_dt, 1)
                    the_format=False
                    print("et la")
        else:
            if check == format:      
                files.append(filename)
                self.dismiss_popup()
                print("b")
                self._popup = Popup(title='Information',content=Label(text='Chargement Réussi'),size_hint=(0.5,0.5))
                self._popup.open()
                Clock.schedule_once(self.dismiss_popup_dt, 1)
            else:
                self._popup = Popup(title='Erreur',content=Label(text='Mauvais Format,reesayez'),size_hint=(0.5,0.5))
                self._popup.open()
                Clock.schedule_once(self.dismiss_popup_dt, 1)

        if the_format and len(files)!=0:
            if check == format:
                if format==".fna" and compteur ==1:
                    if name==filename:
                        self._popup = Popup(title='Erreur',content=Label(text='Fichier deja chargé,reesayez'),size_hint=(0.5,0.5))
                        self._popup.open()
                        Clock.schedule_once(self.dismiss_popup_dt, 1)
                    else:
                        files.append(filename)
                        print("rela")
                        self.dismiss_popup()
                        self._popup = Popup(title='Information',content=Label(text='Chargement Réussi'),size_hint=(0.5,0.5))
                        self._popup.open()
                        Clock.schedule_once(self.dismiss_popup_dt, 1)
                else:
                    files.append(filename)
                    self.dismiss_popup()
                    print("b")
                    self._popup = Popup(title='Information',content=Label(text='Chargement Réussi'),size_hint=(0.5,0.5))
                    self._popup.open()
                    Clock.schedule_once(self.dismiss_popup_dt, 1)
            else:
                self._popup = Popup(title='Erreur',content=Label(text='Mauvais Format,reesayez'),size_hint=(0.5,0.5))
                self._popup.open()
                Clock.schedule_once(self.dismiss_popup_dt, 1)   

                    

    
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

    #pas fini
    def show_clear(self):
        content = Choice(yes=self.clear_files, cancel=self.dismiss_popup)
        self._popup = Popup(title="Clear file", content=content,
                            size_hint=(0.4, 0.4))
        self._popup.open()
    
    def clear_files(self):
        self.files.clear()
        

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Choice(FloatLayout):
    yes = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MyApp(App):
    def build(self):
        return MyPanel()



if __name__ == '__main__':
	MyApp().run()

  