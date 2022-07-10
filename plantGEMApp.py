import sys

from kivy.clock import Clock
from cgitb import text
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView

import Graph
import subprocess
import os

Window.size = (1000, 800)

if "linux" in sys.platform:
    root = Builder.load_file("plantGEM.kv")


class MyPanel(TabbedPanel):
    files = {"faa Model": "", "faa Subject": "", "fna": "", "gff": "", "sbml": "", "tsv": "",
             "json": ""}  # dictionary to store files' path according to format
    format = ""  # takes the value of the extension expected by the clicked button
    buttonName = ""  # takes the value of the button id of the clicked button
    module = "Main"  # takes the value of the module of the clicked button
    parametre = {"i": 50.0, "d": 30.0, "ev": 0.0, "c": 20.0, "bs": 300.0,
                 "nom": "draft"}  # dictionary to store values parameters of module
    defaut = {"i": 50, "d": 30, "ev": 0, "c": 20, "bs": 300,
              "nom": "draft"}  # dictionary to store default values parameters of module
    filesName = ""  # take the path of the loaded file
    text_input = ObjectProperty(text)
    type = ObjectProperty(None)
    input = False
    mainDirectory = ""  # take the path of the main directory
    graph = Graph.Graph("")
    options = 1
    cofac = True

    def on_tab_change(self):
        """
        Create a popup after changing tab if files were selected on the previous tab. If the user choose to proceed,
        the files are removed from the selection and he has access to the new tab. If he chooses to cancel the change tab
        event, it reverts to the tab he was previously on and keep the files he selected.
        """
        check = False #this check allow to prevent the popup to appears again if the user choose to stay on the same tab.
        empty_files = all(x == "" for x in self.files.values())
        if not empty_files:
            content = Change_tab(proceed=self.change_tabs,
                                 cancel=self.stay_same_tab)  # define the content of the pop-up
            self._popup = Popup(title="Load file", content=content,
                                size_hint=(0.8, 0.8), auto_dismiss=False)
            self._popup.open()
            check = True
        if not check:
            self.module = self.get_current_tab().text

    def change_tabs(self):
        """
        Clear files and label before closing the change tab popup.
        """
        tab = self.get_current_tab()
        self._popup.dismiss()
        for key in self.files.keys():
            self.files[key] = ""
        self.module = tab.text
        self.parametre.update(self.defaut)
        self.clear_graph_data()
        self.ids[
            "files_main"].text = "Currently selected files :\n\nfaa Model :\n\nfaa Subject :\n\nfna :\n\ngff :\n\nsbml :\n\ntsv :"
        self.ids["files_blast"].text = "Currently selected files :\n\nfaa Model :\n\nfaa Subject :\n\ngff :\n\nsbml :"
        self.ids["files_mpwt"].text = "Currently selected files :\n\nfna :\n\ngff :\n\ntsv :"

    def stay_same_tab(self):
        """
        Go back to the tab the user was previously on before closing the popup.
        """
        self.dismiss_popup()
        for index, tab in enumerate(self.tab_list):
            if self.module == tab.text:
                self.switch_to(self.tab_list[index])
                self.module = self.get_current_tab().text
                self.dismiss_popup()

    def dismiss_popup(self):
        """
        Self explanatory function
        """
        self._popup.dismiss()

    def dismiss_popup_dt(self, dt):
        """
        Dismiss the popup after a certain time.
        :param dt: duration of the popup.
        """
        self._popup1.dismiss()

    def loaded_files(self):
        """
        Update the label of each module each time a file is uploaded or updated.
        """
        if self.module == "Main":
            self.ids["files_main"].text = "Currently selected files :\n\n"
            for item in self.files.items():
                if item[0] != "json":
                    path = str(item[1]).replace("\\", "/")
                    path = path.split("/")
                    name = path[-1]
                    self.ids["files_main"].text += f"{item[0]} : {name}\n\n"

        if self.module == "BLASTing":
            self.ids["files_blast"].text = "Currently selected files :\n\n"
            for item in self.files.items():
                if item[0] == "faa Model" and item[0] == "faa Subject" and item[0] == "gff" or item[0] == "sbml":
                    path = item[1].replace("\\", "/")
                    path = path.split("/")
                    name = path[-1]
                    self.ids["files_blast"].text += f"{item[0]} : {name}\n\n"
        if self.module == "MPWTing":
            self.ids["files_mpwt"].text = "Currently selected files :\n\n"
            for item in self.files.items():
                if item[0] == "gff" or item[0] == "fna" or item[0] == "tsv":
                    path = item[1].replace("\\", "/")
                    path = path.split("/")
                    name = path[-1]
                    self.ids["files_mpwt"].text += f"{item[0]} : {name}\n\n"

    def show_load(self, textName, extension, instance):
        """
        Open the file explorer
        :param textName: name of the button
        :param extension: extension associated with the file the user need to enter.
        :param instance: the button that launched this function
        :return:
        """
        self.buttonName = textName
        self.format = extension
        content = LoadDialog(load=self.load_file, cancel=self.dismiss_popup)  # define the content of the pop-up
        self._popup = Popup(title=f"Select {instance.file} file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load_dir(self, dirname):
        self.mainDirectory = dirname[0]


    def load_file(self, path, filename):
        """
        get the path to the file and its name from the filechooser, checks its format and add it to the file list.
        If no file choose, raises an error popup.
        :param path: path to the selected file.
        :param filename: name of the selected file.
        """
        if filename:
            with open(os.path.join(path, filename[0])) as stream:
                self.text_input.text = stream.read()
            self.filesName = filename[0]
            verifie = self.check_format()
            if verifie:
                self.dismiss_popup()
            extension = filename[0].split(".")
            self.loaded_files()
            if extension[1] == "json":
                self.graph.update_data(filename[0])
                self.toggle_meta_list()
                self.toggle_reac_list()
        else:
            self._popup1 = Popup(title="No files !", content=Label(text="You did not chose any files !"),
                                 size_hint=(0.4, 0.4))
            self._popup1.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)



    def check_format(self):
        """check if the extension of the uploaded file is the extension expected by the clicked button
            if the extension is the good , the path id added to the dictionnary files at the corresponding key,
            else the function alerts the user of his error.
            If a file already exists for the extension then it is replaced """
        good_format = False
        extension = self.filesName.split(".")
        if extension[1] == self.format:
            for key in self.files.keys():
                if key == self.buttonName:
                    if self.files.get(key) != "":
                        self._popup1 = Popup(title="Replace files", content=Label(text="Updated File"),
                                             size_hint=(0.4, 0.4))
                        self._popup1.open()
                        Clock.schedule_once(self.dismiss_popup_dt, 2)
                        self.files[key] = self.filesName
                        good_format = True
                    else:
                        self.files[key] = self.filesName
                        self._popup1 = Popup(title="Replace files", content=Label(text="File successfully loaded ..."),
                                             size_hint=(0.4, 0.4))
                        self._popup1.open()
                        Clock.schedule_once(self.dismiss_popup_dt, 2)
                        self.files[key] = self.filesName
                        good_format = True

        else:
            self._popup1 = Popup(title='Error', content=Label(text='Please choose the right format'),
                                 size_hint=(0.5, 0.5))
            self._popup1.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)
        return good_format

    def choosedirectory(self):
        """
        File explorer popup to choose a directory.
        """
        content = LoadDialog(load=self.load_dir, cancel=self.dismiss_popup)  # define the content of the pop-up
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def temp_dir(self):
        """
        create a temporary directory "temp_dir" with all the files uploaded.
        """
        os.mkdir("temp_dir")
        for key in self.files.keys():
            os.system(f"cp {self.files[key]} temp_dir")



    def go_module(self):
        """ check if the main directory exists and if the all necessary files are downloaded for the module.
            if is true , the module is run , else the function alerts the user of his error by raising a popup"""
        check_value = True
        message = ""
        empty_dict = all(x == "" for x in self.files.values())

        if self.module == "BLASTing" or self.module == "Main":
            if self.mainDirectory == "" and empty_dict:
                check_value = False
                message += "Please enter a main directory\n\n"

        if self.module == "BLASTing":
            if self.files.get("faa Subject") != "" and self.files.get("faa Model") != "" and self.files.get(
                    "gff") != "" and self.files.get("sbml") != "":
                if self.files.get("faa Subject") == self.files.get("faa Model"):
                    check_value = False
                    message += "Fasta files must be different\n\n"
            else:
                message += "Please load all necessary files\n\n"
                check_value = False
            if check_value:
                self.launch_module()
            else:
                self._popup1 = Popup(title='Error', content=Label(text=message),
                                     size_hint=(0.5, 0.5))
                self._popup1.open()
                Clock.schedule_once(self.dismiss_popup_dt, 1)

        if self.module == "MPWTing":
            if self.files.get("tsv") != "" and self.files.get("fna") != "" and self.files.get("gff") != "":
                self.launch_module()
            else:
                message += "Please load all necessary files\n\n"

        if self.module == "Main":
            if self.files.get("faa Subject") != "" and self.files.get("faa Model") != "" and self.files.get(
                    "gff") != "" and self.files.get("sbml") != "" and self.files.get("fna") != "" and self.files.get(
                "tsv") != "":
                if self.files.get("faa Model") == self.files.get("faa Subject"):
                    message += "Fasta files must be different\n\n"
                    check_value = False
            else:
                message += "Please load all necessary files\n\n"
                check_value = False
            if check_value:
                self.launch_module()
            else:
                self._popup1 = Popup(title='Error', content=Label(text=message),
                                     size_hint=(0.5, 0.5))
                self._popup1.open()
                Clock.schedule_once(self.dismiss_popup_dt, 2)

    def module_merge(self):
        """
        Launch the merge module, raises a popup if no directory was selected.
        """
        self.module = "Merging"
        if self.mainDirectory == "":
            self._popup1 = Popup(title='Error', content=Label(text='Please enter a main directoryt'),
                                 size_hint=(0.5, 0.5))
            self._popup1.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)
        else:
            self.launch_module()



    def launch_module(self):
        """check the current module and launches the command line related to the module using subprocess library"""
        cmd = ""
        if self.module == "Merging":
            cmd = f"python3 merging.py {self.mainDirectory}"
        if self.module == "BLASTing":
            cmd = f"python3 blasting.py {self.mainDirectory} -n {self.parametre['nom']} -m {self.files['sbml']} -mfaa {self.files['faa Model']} -sfaa {self.files['faa Subject']} -sgff {self.files['gff']} -i {self.parametre['i']} -d {self.parametre['d']} -ev {self.parametre['ev']} -c {self.parametre['c']} -bs {self.parametre['bs']}"
        if self.module == "MPWTing":
            cmd = f"python3 "
        if self.module == "Main":
            self.temp_dir()
            cmd = f"python3 main.py {self.mainDirectory} -m {self.files['sbml']} -mfaa {self.files['faa Model']} -sfaa {self.files['faa Subject']} -sgff {self.files['gff']} -i {self.parametre['i']} -d {self.parametre['d']} -ev {self.parametre['ev']} -c {self.parametre['c']} -bs {self.parametre['bs']} "
        p = subprocess.Popen(cmd, shell=True)
        p.wait()
        os.system("rm -rf ./temp_dir/")
        if p.returncode == 0:
            print('command : success')
        else:
            print('command : fail')
        self.files.clear()


    def show_param(self):
        """
        Open the popup to choose the different launch parameters of Main and Blast module.
        """
        content = Parameters(cancel=self.dismiss_popup)
        self._popup = Popup(title="Enter Parameters", content=content, size_hint=(1, 1))
        self._popup.open()

    def toggle_compartment_list(self):
        """
        Display or not the list of comprtment
        :return:
        """
        if self.ids["compartment_list"].opacity == 0:
            self.ids["compartment_list"].opacity = 1
            if MyPanel.graph.data:
                self.ids["compartment_list"].data = [{"text": compartment, "root_widget": self.ids["compartment_list"]}
                                                     for compartment in
                                                     MyPanel.graph.compartment]
        else:
            self.ids["compartment_list"].opacity = 0

    def clear_graph_data(self):
        """
        Clear the current search for Metabolites and Reactions.
        """
        self.ids["keywords"].text = "Currently in search :\n\nMetabolites :\n\nReactions:\n\nCompartment:\n"
        self.graph.clear_data()

    def pop_up_save_graph(self, instance):
        """
        Open the file explorer to choose where to save the graph.
        :param instance: Either SAVE or SHOW graph, change the name of the popup and the text input.
        """
        if instance.type == "html":
            content = Save_dialog(save=self.show_graph, cancel=self.dismiss_popup,
                                  text="graph.html")  # define the content of the pop-up
            self._popup = Popup(title="Save html file", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()
        if instance.type == "json":
            content = Save_dialog(save=self.save_graph, cancel=self.dismiss_popup,
                                  text="graph.json")  # define the content of the pop-up
            self._popup = Popup(title="Save html file", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()

    def show_graph(self, path, filename):
        """
        launch the function to create and draw the graph.
        :param path: path to the directory where you want to save the graph html file.
        :param filename: name of the saved html file.
        """
        if "." in filename:
            extension = filename.split('.')
            if "html" != extension[1]:
                filename = extension[0] + ".html"
        else:
            filename = filename + ".html"
        complete_path = path + "/" + filename
        if self.graph.data:
            self.graph.create_Graph(complete_path, self.cofac, self.options)
        else:
            self._popup1 = Popup(title='Error', content=Label(text="Please load a file first"),
                                 size_hint=(0.5, 0.5))
            self._popup1.open()
            Clock.schedule_once(self.dismiss_popup_dt, 2)

    def save_graph(self, path, filename):
        """
        launch the function to save the graph as json format.
        :param path: path to the directory where you want to save the graph json file.
        :param filename: name of the saved json file.
        """
        if "." in filename:
            extension = filename.split('.')
            if "json" != extension[1]:
                filename = extension[0] + ".html"
        else:
            filename = filename + ".html"
        complete_path = path + "/" + filename
        if self.graph.data:
            self.graph.save_graph_json(complete_path)
        else:
            self._popup1 = Popup(title='Error', content=Label(text="Please draw a graph first"),
                                 size_hint=(0.5, 0.5))
            self._popup1.open()
            Clock.schedule_once(self.dismiss_popup_dt, 2)

    def toggle_meta_list(self):
        """
        Show and update the RecycleView for all the metabolites or a selection if a compartment was selected and/or
        if you started typing the name of the metabolites you want to add to the graph.
        """
        temp_compartment = [Graph.cobra_compatibility(reac, False) for reac in MyPanel.graph.search_compartment]
        if self.ids["Meta_list"].opacity == 0 and self.graph.data:
            if self.graph.search_compartment:
                self.ids["Meta_list"].data = [{"text": meta["id"], "root_widget": self.ids["Meta_list"]} for meta in
                                              self.graph.data["metabolites"] if
                                              meta["compartment"] in temp_compartment]

            else:
                if not self.ids["TI_meta"].text:
                    self.ids["Meta_list"].data = [{"text": meta["id"], "root_widget": self.ids["Meta_list"]} for
                                                  meta in
                                                  self.graph.data["metabolites"]]
                else:
                    self.ids["Meta_list"].data = [{"text": meta["id"], "root_widget": self.ids["Meta_list"]} for
                                                  meta in self.graph.data["metabolites"] if
                                                  self.ids["TI_meta"].text.upper() in meta["id"].upper()]
            self.ids["Meta_list"].opacity = 1
        else:
            self.ids["Meta_list"].opacity = 0

    def toggle_reac_list(self):
        """
        Show and update the RecycleView for all the reaction or a selection if you started typing the name
        of the reaction you want to add to the graph.
        """
        if self.ids["Reac_list"].opacity == 0:
            self.ids["Reac_list"].opacity = 1
            if MyPanel.graph.data:
                if not self.ids["TI_reac"]:
                    self.ids["Reac_list"].data = [{"text": reac["id"], "root_widget": self.ids["Reac_list"]} for reac in
                                                  MyPanel.graph.data["reactions"]]
                else:
                    self.ids["Reac_list"].data = [{"text": reac["id"], "root_widget": self.ids["Reac_list"]} for reac in
                                                  MyPanel.graph.data["reactions"] if
                                                  self.ids["TI_reac"].text.upper() in reac["id"].upper()]
        else:
            self.ids["Reac_list"].opacity = 0

    def change_option(self, instance):
        """
        Change between the 3 physics mode and if you want or not add the cofactors to the graph.
        :param instance: button that was pressed in the "Disply options" popup.
        """
        if instance.type == "default":
            MyPanel.options = 1
            self.ids["physics_options"].text = "Physics mode selected : \n\nDefault"
        if instance.type == "dynamic":
            MyPanel.options = 2
            self.ids["physics_options"].text = "Physics mode selected : \n\nDynamic"
        if instance.type == "no_physics":
            MyPanel.options = 3
            self.ids["physics_options"].text = "Physics mode selected : \n\nNo Physics"
        if instance.type == "Yes":
            MyPanel.cofac = True
            self.ids["cofactors_selection"].text = "Cofactors displayed : Yes"
            if MyPanel.files["json"] != "":
                MyPanel.graph.update_data(MyPanel.files["json"])
        if instance.type == "No":
            MyPanel.cofac = False
            if MyPanel.files["json"] != "":
                MyPanel.graph.update_data(MyPanel.files["json"])
            self.ids["cofactors_selection"].text = "Cofactors displayed : No"

    def select_options(self):
        """
        Open the Display Options popup.
        """
        content = Physics(select=self.change_option)
        self._popup = Popup(title="Set graph display options", content=content, size_hint=(0.7, 0.7), title_size=16)
        self._popup.open()


class Physics(FloatLayout):
    select = ObjectProperty(None)


class Load_Button(Button):
    file = ObjectProperty(None)


# define the object load dialog
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Save_dialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)
    text = ObjectProperty(None)


class Change_tab(FloatLayout):
    cancel = ObjectProperty(None)
    proceed = ObjectProperty(None)


class DirectoryName(BoxLayout):
    cancel = ObjectProperty(None)

    def add_directory(self, inputname):
        valeur = self.ids[inputname].text
        if valeur != "":
            MyPanel.mainDirectory = valeur


# define the object settings dialog
class Parameters(BoxLayout):
    cancel = ObjectProperty(None)



    def add_value(self, param, id):
        """check if the value in textinput is in the interval, if is true the value of the dictionnary parameter is replace,
            else the function alerts the user of his error by raising a popup"""
        valeur = self.ids[id].text
        if id == "input6":
            MyPanel.parametre[param] = valeur
        try:
            if valeur != "":
                value = float(valeur)
                if param == "ev" and 1 >= value >= 0:
                    MyPanel.parametre['ev'] = value
                elif param == "i" and 100 >= value >= 0:
                    MyPanel.parametre['i'] = value
                elif param == "d" and 100 >= value >= 0:
                    MyPanel.parametre['d'] = value
                elif param == "c" and 100 >= value >= 0:
                    MyPanel.parametre['c'] = value
                elif param == "bs" and 1000 >= value >= 0:
                    MyPanel.parametre['bs'] = value
                else:
                    self._popup = Popup(title='Error', content=Label(text="The entered value is not within the range"),
                                        size_hint=(0.5, 0.5))
                    self._popup.open()
        except:
            self._popup = Popup(title='Error', content=Label(text="Value is not numeric "), size_hint=(0.5, 0.5))
            self._popup.open()


    def reset(self):
        """
        Set the parameters to their default value.
        """
        MyPanel.parametre.update(MyPanel.defaut)


class TI_meta(TextInput):

    def on_text(self,instance, value):
        """
        update the list of metabolites shown in the RecycleView as the text in the textinput changes.
        :param value: the characters curretnly written in the textinput box.
        """
        meta_list = App.get_running_app().root.ids["Meta_list"]
        if meta_list.data:
            meta_list.data = [
                {"text": meta["id"], "root_widget": App.get_running_app().root.ids["Meta_list"]} for
                meta in MyPanel.graph.data["metabolites"] if
                value.upper() in meta["id"].upper()]
            if meta_list.opacity == 0:
                meta_list.opacity = 1


class TI_reac(TextInput):

    def on_text(self,instance, value):
        """
        update the list of reactions shown in the RecycleView as the text in the textinput changes.
        :param value: the characters curretnly written in the textinput box.
        """
        if App.get_running_app().root.ids["Reac_list"].data:
            App.get_running_app().root.ids["Reac_list"].data = [
                {"text": reac["id"], "root_widget": App.get_running_app().root.ids["Reac_list"]} for
                reac in MyPanel.graph.data["reactions"] if
                value.upper() in reac["id"].upper()]


class Compartment_buttons(Button):
    root_widget = ObjectProperty()

    def on_release(self):
        """
        add button properties to the fake buttons of the RecycleView widget.
        """
        super().on_release()
        self.root_widget.btn_callback(self)


class Meta_list_buttons(Button):
    root_widget = ObjectProperty()

    def on_release(self, **kwargs):
        """
        add button properties to the fake buttons of the RecycleView widget.
        """
        super().on_release()
        self.root_widget.btn_callback(self)


class Meta_List(RecycleView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if MyPanel.graph.data:
            self.data = [{"text": meta["id"], 'root_widget': self} for meta in MyPanel.graph.data["metabolites"]]

    def selected_keyword(self):
        message = f"Currently in search :\n\nMetabolites : {', '.join(MyPanel.graph.meta_keyword)}\n\nReactions : " \
                  f"{', '.join(MyPanel.graph.reac_keyword)}\n\nCompartments : {', '.join(MyPanel.graph.search_compartment)}"
        App.get_running_app().root.ids["keywords"].text = message

    def btn_callback(self, btn):
        if self.opacity == 1:
            MyPanel.graph.meta_keyword_update(btn.text)
            self.selected_keyword()


class Reac_list_buttons(Button):
    root_widget = ObjectProperty()

    def on_release(self, **kwargs):
        """
        add button properties to the fake buttons of the RecycleView widget.
        """
        super().on_release()
        self.root_widget.btn_callback(self)


class Reac_List(RecycleView):
    def __init__(self, **kwargs):
        super(Reac_List, self).__init__(**kwargs)
        if MyPanel.graph.data:
            self.data = [{"text": reac["id"], 'root_widget': self} for reac in MyPanel.graph.data["reactions"]]

    def selected_keyword(self):
        """
        Update the label that allows the user to see which reactions he added to the search.
        """
        message = f"Currently in search :\n\nMetabolites : {', '.join(MyPanel.graph.meta_keyword)}\n\nReactions : " \
                  f"{', '.join(MyPanel.graph.reac_keyword)}\n\nCompartments : {', '.join(MyPanel.graph.search_compartment)}"
        App.get_running_app().root.ids["keywords"].text = message

    def btn_callback(self, btn):
        """
        Add the reactions to the search list.
        """
        if self.opacity == 1:
            MyPanel.graph.reac_keyword_update(btn.text)
            self.selected_keyword()


class Compartment_List(RecycleView):
    def __int__(self, **kwargs):
        super(Compartment_List, self).__init__(**kwargs)
        if MyPanel.graph.data:
            self.data = [{"text": comp["id"], 'root_widget': self} for comp in MyPanel.graph.data["compartment"]]

    def selected_keyword(self):
        """
        Update the label that allows the user to see which reactions he added to the search.
        """
        message = f"Currently in search :\n\nMetabolites : {', '.join(MyPanel.graph.meta_keyword)}\n\nReactions : " \
                  f"{', '.join(MyPanel.graph.reac_keyword)}\n\nCompartments : {', '.join(MyPanel.graph.search_compartment)}"
        App.get_running_app().root.ids["keywords"].text = message

    def update_meta_list(self):
        """
        Update the metabolites list depending on the compartment chosen by the user.
        """
        temp_compartment = [Graph.cobra_compatibility(reac, False) for reac in MyPanel.graph.search_compartment]
        meta_list = App.get_running_app().root.ids["Meta_list"]#to get ids from a class that is not the main class of the app.
        if meta_list.data:
            meta_list.data = []
            meta_list.data = [
                {"text": meta["id"], "root_widget": meta_list} for
                meta in MyPanel.graph.data["metabolites"] if
                meta["compartment"] in temp_compartment]
        if not MyPanel.graph.search_compartment:
            if not App.get_running_app().root.ids["TI_meta"].text:
                meta_list.data = [{"text": meta["id"], "root_widget": meta_list} for
                                  meta in
                                  MyPanel.graph.data["metabolites"]]
            else:
                meta_list.data = [{"text": meta["id"], "root_widget": meta_list} for
                                  meta in MyPanel.graph.data["metabolites"] if
                                  App.get_running_app().root.ids["TI_meta"].text.upper() in meta["id"].upper()]

    def btn_callback(self, btn):
        """
        Add the reactions to the search list.
        """
        if self.opacity == 1:
            MyPanel.graph.compartment_update(btn.text)
            self.selected_keyword()
            self.update_meta_list()


class plantGEMApp(App):

    def build(self):
        return MyPanel()
