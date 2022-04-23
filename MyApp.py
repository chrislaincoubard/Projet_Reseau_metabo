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
    files_blast=[]
    files_mpwting=[]
    compteur_fasta=0
    compteur_sbml=0
    text_input = ObjectProperty(text)

    def dismiss_popup(self):
        self._popup.dismiss()


####    MAIN   ####

    def show_load_main(self):
        content = LoadDialog(load=self.load_main, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
        
####### Fonction Load ( sert de main pour le blast) #######

    def load_main(self, path, filename):
        #compteur=0
        #listdir(fn)
        for i in range (7):
            with open(os.path.join(path, filename[0])) as stream:
                self.text_input.text = stream.read()
        self.dismiss_popup()
        
    

####    BLAST   ####

    def show_load_blast(self):
        content = LoadDialog(load=self.load_blast, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
        
####### Fonction Load ( sert de main pour le blast) #######

    def load_blast(self, path, filename):
        compteur=0
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
        self.dismiss_popup()
        
        self.check_fastaOrSbml(filename,self.files_blast)
        
        for i in range(len(self.files_blast)):
            compteur+=1
            if compteur == 3:
                verifie = self.check_files_blast(self.files_blast)
                if verifie:
                    self.launch_blasting(self.files_blast)
                    
                else:
                    self.files_blast.clear()
                    self._popup = Popup(title='Erreur',content=Label(text='Mauvais Fichiers , recommncez la sélection'),size_hint=(0.5,0.5))



####### Verifie le format des fichiers pour le blast #######

    
    def check_fastaOrSbml(self, filename,files_blast):
        
        check = filename[0][-5:]
        if check == "fasta" or check==".sbml":
            files_blast.append(filename)
        else:
            self.dismiss_popup()
            self._popup = Popup(title='Erreur',content=Label(text='Mauvais Format'),size_hint=(0.5,0.5))
            self._popup.open()
            
####### Verifie le format la liste de fichiers BLAST #######


    def check_files_blast(files_blast):
        go_blast=False
        compteur_fasta=0
        compteur_sbml=0
        for i in range[files_blast]:
            if  files_blast[i][-5:] == "fasta":
                compteur_fasta+=1 
            if files_blast[i][-5:] ==".sbml":
                compteur_sbml+=1
        if compteur_fasta==2 and compteur_sbml==1:
            go_blast=True
        for i in range[files_blast]:
            if files_blast[1] == files_blast[2]:
                go_blast=False
            if files_blast[3] == files_blast[2]:
                go_blast=False
            if files_blast[1] == files_blast[3]:
                go_blast=False
        return (go_blast)


####### Lance le script BLAST #######

    def launch_blasting(files_blast):
        cmd = f"python3 blasting.py {files_blast[0]} {files_blast[1]} {files_blast[2]}"
        p = subprocess.Popen(cmd, shell = True)
        p.wait()
        if p.returncode == 0 :
            print('command : success')
        else :
            print('command : fail')

#####   MPWTING ####

    def show_load_mpwting(self):
        content = LoadDialog(load=self.load_mpwting, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

####### Fonction Load ( sert de main pour le mpwting) #######

    def load_mpwting(self, path, filename):
        compteur=0
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
        self.dismiss_popup()
        
        self.check_format(filename,self.files_mpwting)
        
        for i in range(len(self.files_mpwting)):
            compteur+=1
            if compteur == 3:
                verifie = self.check_files_mpwting(self.files_mpwting)
                if verifie:
                    self.launch_mpwting(self.files_mpwting)
                    
                else:
                    self.files_mpwting.clear()
                    self._popup = Popup(title='Erreur',content=Label(text='Mauvais Fichiers , recommncez la sélection'),size_hint=(0.5,0.5)) 

####### Verifie le format des fichiers pour le mpwting #######

    def check_format(self, filename,files_mpwting):
        
        check = filename[0][-4:]
        if check == ".fna" or check==".gff" or check==".tsv":
            files_mpwting.append(filename)
        else:
            self.dismiss_popup()
            self._popup = Popup(title='Erreur',content=Label(text='Mauvais Format'),size_hint=(0.5,0.5))
            self._popup.open()     

####### Verifie le format la liste de fichiers MPWTing #######

    def check_files_mpwting(files_mpwting):
        go_mpwting=False
        compteur_fna=0
        compteur_gff=0
        compteur_tsv=0
        for i in range[files_mpwting]:
            if  files_mpwting[i][-4:] == ".fna":
                compteur_fna+=1 
            if files_mpwting[i][-4:] ==".gff":
                compteur_gff+=1
            if files_mpwting[i][-4:] ==".tsv":
                compteur_tsv+=1    
        if compteur_fna==1 and compteur_gff==1 and compteur_tsv==1:
            go_mpwting=True
        
        return (go_mpwting)

####### Lance le script MPWTING #######

    def launch_mpwting(files_mpwting):
            cmd = f"python3 mpwting.py {files_mpwting[0]} {files_mpwting[1]} {files_mpwting[2]}"
            p = subprocess.Popen(cmd, shell = True)
            p.wait()
            if p.returncode == 0 :
                print('command : success')
            else :
                print('command : fail')


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MyApp(App):
    def build(self):
        return MyPanel()


if __name__ == '__main__':
    MyApp().run() 