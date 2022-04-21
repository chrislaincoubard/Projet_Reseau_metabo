# -*- coding: utf-8 -*-

from cgitb import text
from distutils.command.build import build
from time import sleep
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.tabbedpanel import TabbedPanel
from  kivy.uix.label import Label
import subprocess
import os


class MyPanel(TabbedPanel):
    files=[]
    compteur_fasta=0
    compteur_sbml=0
    text_input = ObjectProperty(text)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
        

    def load(self, path, filename):
        compteur=0
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
        self.dismiss_popup()
        
        self.check_fastaOrSbml(filename,self.files)
        
        for i in range(len(self.files)):
            compteur+=1
            if compteur == 3:
                verifie = self.check_files()
                if verifie:
                    self.launch_blasting(self.files)
                    
                else:
                    self.files.clear()
                    self._popup = Popup(title='Erreur',content=Label(text='Mauvais Fichiers , recommncez la sélection'),size_hint=(0.5,0.5))

    def launch_blasting(files):
        cmd = f"python3 blasting.py {files[0]} {files[1]} {files[2]}"
        p = subprocess.Popen(cmd, shell = True)
        p.wait()
        if p.returncode == 0 :
            print('command : success')
        else :
            print('command : fail')
    
    def check_fastaOrSbml(self, filename,files):
        
        
        check = filename[0][-5:]
        if check == "fasta" or check==".sbml":
            files.append(filename)
        else:
            self.dismiss_popup()
            self._popup = Popup(title='Erreur',content=Label(text='Mauvais Format'),size_hint=(0.5,0.5))
            self._popup.open()
            


    def check_files(files):
        go_blast=False
        compteur_fasta=0
        compteur_sbml=0
        for i in range[files]:
            if  files[i][-5:-0] == "fasta":
                compteur_fasta+=1 
            if files[i][-5:-0] ==".sbml":
                compteur_sbml+=1
        if compteur_fasta==2 and compteur_sbml==1:
            go_blast=True
        for i in range[files]:
            if files[1] == files[2]:
                go_blast=False
            if files[3] == files[2]:
                go_blast=False
            if files[1] == files[3]:
                go_blast=False
        return (go_blast)
             
        
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MyApp(App):
    def build(self):
        return MyPanel()


if __name__ == '__main__':
    MyApp().run() 