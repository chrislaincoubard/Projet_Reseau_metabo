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
from kivy.clock import Clock
import subprocess
import os


class MyPanel(TabbedPanel):
    files_blast=[]
    files_mpwting=[]
    files_main=[]
    compteur_fasta=0
    compteur_sbml=0
    text_input = ObjectProperty(text)

    def dismiss_popup_dt(self, dt):
        self._popup.dismiss()

    def dismiss_popup(self):
        self._popup.dismiss()


####    MAIN   ####


#### MAIN FILES ####


#### Boites Load files   ####

    def show_load_files_main(self):
        content = LoadDialog(load=self.load_files_main, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                                size_hint=(0.9, 0.9))
        self._popup.open()
        for i in reversed (range(0,5)):
            content = LoadDialog(load=self.load_files_main, cancel=self.dismiss_popup)
            self._popup = Popup(title="Load file", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()
            converted_i=str(i)
            converted_I=str(i+1)
            if i ==0:
                self._popup1=Popup(title='Information',content=Label(text="Vous devez charger 6 fichiers (.faa , .tsv, .gff , .sbml , .fasta et .fasta"),size_hint=(0.8,0.3))
                self._popup1.open()
            else:
                self._popup1=Popup(title='Information',content=Label(text='Fichier' +converted_i+' chargé, selectionnez le fichier '+converted_I),size_hint=(0.5,0.5))
                self._popup1.open()
                   
        
####### Fonction Load Files ( sert de main ) #######

    def load_files_main(self, path, filename):
        #compteur=0
        #listdir(fn)
        
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
        print(filename)
        

        verifie=self.check_all(filename,self.files_main)
        if verifie:
            self.dismiss_popup()
            self.launch_main(self.files_main)
        

#### Verifie au fur et à mesure de la selection le format des fichiers #### 
    def check_all(self,filename,files_main):
        check=False
        format=[".fna",".tsv",".gff","sbml"]
        compteur_fasta=0
        good_format=False
        print(filename,filename[0][-5:])
        if filename[0][-4:] not in format and filename[0][-5:] != "fasta":
            self._popup = Popup(title='Erreur',content=Label(text='Mauvais Format , recommencez'),size_hint=(0.5,0.5))
            self._popup.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)

        else: 
            if filename[0][-5:] == "fasta":
                for i in files_main:
                    if i[0][-5:]=="fasta":
                        compteur_fasta+=1
                if compteur_fasta>2:
                    self._popup = Popup(title='Erreur',content=Label(text='Format déjà chargé, recommencez'),size_hint=(0.5,0.5))
                    self._popup.open()
                    Clock.schedule_once(self.dismiss_popup_dt, 1)
                else:
                    files_main.append(filename)
                    check=True
            else:
                for i in format:
                    if i[0][-4:] == filename[0][-4:] and filename[0][-5:] != "fasta":
                        self._popup = Popup(title='Erreur',content=Label(text='Format déjà chargé, recommencez'),size_hint=(0.5,0.5))
                        self._popup.open()
                        Clock.schedule_once(self.dismiss_popup_dt, 1)
                    else:
                        good_format=True
                if good_format==True:
                    files_main.append(filename)
                    check=True
        return check

#### Lance le main ####

    def launch_main(files_main):
        cmd = f"python3 blasting.py {files_main[0]} {files_main[1]} {files_main[2]} {files_main[3]} {files_main[4]} {files_main[5]}"
        p = subprocess.Popen(cmd, shell = True)
        p.wait()
        if p.returncode == 0 :
            print('command : success')
        else :
            print('command : fail')



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
        
        
        next=self.check_fastaOrSbml(filename,self.files_blast)
        if next:
            self.dismiss_popup()

        for i in range(len(self.files_blast)):
            compteur+=1
            if compteur == 3:
                verifie = self.check_files_blast(self.files_blast)
                if verifie:
                    self.launch_blasting(self.files_blast)
                    
                else:
                    self.files_blast.clear()
                    self._popup = Popup(title='Erreur',content=Label(text='Mauvais Fichiers , recommencez la sélection'),size_hint=(0.5,0.5))
                    Clock.schedule_once(self.dismiss_popup_dt, 1)



####### Verifie le format des fichiers pour le blast #######

    
    def check_fastaOrSbml(self, filename,files_blast):
        good_format=False
        check = filename[0][-5:]
        if check == "fasta" or check==".sbml":
            files_blast.append(filename)
            self._popup = Popup(title='Erreur',content=Label(text='Chargement réussi'),size_hint=(0.5,0.5))
            self._popup.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)
            good_format=True
        else:
            good_format=False
            self._popup = Popup(title='Erreur',content=Label(text='Mauvais Format,recommencez'),size_hint=(0.5,0.5))
            self._popup.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)
        return good_format
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
        
        
        next=self.check_format(filename,self.files_mpwting)
        if next:
            self.dismiss_popup()
        for i in range(len(self.files_mpwting)):
            compteur+=1
            if compteur == 3:
                verifie = self.check_files_mpwting(self.files_mpwting)
                if verifie:
                    self.launch_mpwting(self.files_mpwting)
                    
                else:
                    self.files_mpwting.clear()
                    self._popup = Popup(title='Erreur',content=Label(text='Mauvais Fichiers , recommencez la sélection'),size_hint=(0.5,0.5))
                    Clock.schedule_once(self.dismiss_popup_dt, 1) 

####### Verifie le format des fichiers pour le mpwting #######

    def check_format(self, filename,files_mpwting):
        good_format=False
        check = filename[0][-4:]
        if check == ".fna" or check==".gff" or check==".tsv":
            files_mpwting.append(filename)
            self._popup = Popup(title='Erreur',content=Label(text='Chargement réussi'),size_hint=(0.5,0.5))
            self._popup.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)
            good_format=True
        else:
            good_format=False
            self._popup = Popup(title='Erreur',content=Label(text='Mauvais Format, recommencez'),size_hint=(0.5,0.5))
            self._popup.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)
        return good_format     

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