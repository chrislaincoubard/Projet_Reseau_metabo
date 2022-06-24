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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView

import Graph
import subprocess
import os

Window.size = (1000, 800)

if "linux" in sys.platform:
    root = Builder.load_file("plantGEM.kv")


class MyPanel(TabbedPanel):
    files = {"faaM": "", "faaS": "", "fna": "", "gff": "", "sbml": "", "tsv": "",
             "json": ""}  # dictionary to store file names according to format
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
    check_bubble = False
    options = 1
    cofac = False

    def on_tab_change(self):
        pop = False
        empty_files = all(x == "" for x in self.files.values())
        # and self.old_module == self.get_current_tab().text
        if not empty_files:
            content = Change_tab(proceed=self.change_tabs,
                                 cancel=self.stay_same_tab)  # define the content of the pop-up
            self._popup = Popup(title="Load file", content=content,
                                size_hint=(0.8, 0.8), auto_dismiss=False)
            self._popup.open()
            pop = True
        if not pop:
            self.module = self.get_current_tab().text

    def change_tabs(self):
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
        self.dismiss_popup()
        for index, tab in enumerate(self.tab_list):
            if self.module == tab.text:
                self.switch_to(self.tab_list[index])
                self.module = self.get_current_tab().text
                self.dismiss_popup()

    # close a pop-up
    def dismiss_popup(self):
        self._popup.dismiss()

    # close a pop-up after dt time
    def dismiss_popup_dt(self, dt):
        self._popup1.dismiss()

    def loaded_files(self):
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
                if item[0] == "faaM" and item[0] == "faaS" and item[0] == "gff" or item[0] == "sbml":
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

    # open the load dialog
    def show_load(self, textName, extension, instance):

        self.buttonName = textName
        self.format = extension
        content = LoadDialog(load=self.load_file, cancel=self.dismiss_popup)  # define the content of the pop-up
        self._popup = Popup(title=f"Select {instance.file} file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load_dir(self, path, dirname):
        self.mainDirectory = dirname[0]

    def get_id(self, instance):
        for id, widget in instance.parent.ids.items():
            if widget.__self__ == instance:
                return id

    # get the path of the uploaded file
    def load_file(self, path, filename):
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
                self.graph.Load_json(filename[0])
                self.toggle_meta_list()
                self.toggle_reac_list()
        else:
            self._popup1 = Popup(title="No files !", content=Label(text="You did not chose any files !"),
                                 size_hint=(0.4, 0.4))
            self._popup1.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)

    """check if the extension of the uploaded file is the extension expected by the clicked button
    if the extension is the good , the path id added to the dictionnary files at the corresponding key,
    else the function alerts the user of his error.
    If a file already exists for the extension then it is replaced """

    def check_format(self):
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
            self._popup1 = Popup(title='Error', content=Label(text='Wrong format, try again'), size_hint=(0.5, 0.5))
            self._popup1.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)
        return good_format

    def choosedirectory(self):
        content = LoadDialog(load=self.load_dir, cancel=self.dismiss_popup)  # define the content of the pop-up
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    # create a temporary directory "temp_dir" with all the files uploaded
    def temp_dir(self):
        os.mkdir("temp_dir")
        for key in self.files.keys():
            os.system(f"cp {self.files[key]} temp_dir")

    """ check if the main directory exists and if the all necessary files are downloaded for the module.
    if is true , the module is run , else the function alerts the user of his error"""

    def go_module(self):
        check_value = True
        message = ""
        empty_dict = all(x == "" for x in self.files.values())

        if self.module == "BLASTing" or self.module == "Main":
            if self.mainDirectory == "" and empty_dict:
                check_value = False
                message += "Please enter a main directory\n\n"

        if self.module == "BLASTing":
            if self.files.get("faaS") != "" and self.files.get("faaM") != "" and self.files.get(
                    "gff") != "" and self.files.get("sbml") != "":
                if self.files.get("faaS") == self.files.get("faaM"):
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
            if self.files.get("faaS") != "" and self.files.get("faaM") != "" and self.files.get(
                    "gff") != "" and self.files.get("sbml") != "" and self.files.get("fna") != "" and self.files.get(
                "tsv") != "":
                if self.files.get("faaM") == self.files.get("faaS"):
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

    # displays an error popup if the maindirectory is empty
    def module_merge(self):
        self.module = "Merging"
        if self.mainDirectory == "":
            self._popup1 = Popup(title='Error', content=Label(text='Please enter a main directoryt'),
                                 size_hint=(0.5, 0.5))
            self._popup1.open()
            Clock.schedule_once(self.dismiss_popup_dt, 1)
        else:
            self.launch_module()

    """check the current module and launches Command Line Interface related to the module using subprocess library"""

    def launch_module(self):
        cmd = ""
        if self.module == "Merging":
            cmd = f"python3 merging.py {self.mainDirectory}"
        if self.module == "BLASTing":
            cmd = f"python3 blasting.py {self.mainDirectory} -n {self.parametre['nom']} -m {self.files['sbml']} -mfaa {self.files['faaM']} -sfaa {self.files['faaS']} -sgff {self.files['gff']} -i {self.parametre['i']} -d {self.parametre['d']} -ev {self.parametre['ev']} -c {self.parametre['c']} -bs {self.parametre['bs']}"
        if self.module == "MPWTing":
            cmd = f"python3 "
        if self.module == "Main":
            self.temp_dir()
            cmd = f"python3 main.py {self.mainDirectory} -m {self.files['sbml']} -mfaa {self.files['faaM']} -sfaa {self.files['faaS']} -sgff {self.files['gff']} -i {self.parametre['i']} -d {self.parametre['d']} -ev {self.parametre['ev']} -c {self.parametre['c']} -bs {self.parametre['bs']} "
        p = subprocess.Popen(cmd, shell=True)
        p.wait()
        os.system("rm -rf ./temp_dir/")
        if p.returncode == 0:
            print('command : success')
        else:
            print('command : fail')
        self.files.clear()

    def callback(self, instance):
        if instance.state == "down":
            self.dismiss_popup()
            self.input = True

    # open the settings dialog
    def show_param(self):
        content = Parameters(cancel=self.dismiss_popup)
        self._popup = Popup(title="Enter Parameters", content=content, size_hint=(1, 1))
        self._popup.open()

    def toggle_compartment_list(self):
        if self.ids["compartment_list"].opacity == 0:
            self.ids["compartment_list"].opacity = 1
            if MyPanel.graph.data:
                self.ids["compartment_list"].data = [{"text": compartment, "root_widget": self.ids["compartment_list"]}
                                                     for compartment in
                                                     MyPanel.graph.compartment]
        else:
            self.ids["compartment_list"].opacity = 0

    def clear_graph_data(self):
        self.ids["keywords"].text = "Currently in search :\n\nMetabolites :\n\nReactions:\n\nCompartment:\n"
        self.graph.clear_data()

    def pop_up_html(self, instance):
        type = instance.type
        if type == "html":
            content = Save_dialog(save=self.show_graph, cancel=self.dismiss_popup,
                                  text="graph.html")  # define the content of the pop-up
            self._popup = Popup(title="Save html file", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()
        if type == "json":
            content = Save_dialog(save=self.save_graph, cancel=self.dismiss_popup,
                                  text="graph.json")  # define the content of the pop-up
            self._popup = Popup(title="Save html file", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()

    def show_graph(self, path, filename):
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

    def toggle_meta_list(self):
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
        if instance.type == "default":
            MyPanel.options = 1
            self.ids["physics_options"].text = "Physics mode selected : \n\n               Default"
        if instance.type == "dynamic":
            MyPanel.options = 2
            self.ids["physics_options"].text = "Physics mode selected : \n\n               Dynamic"
        if instance.type == "no_physics":
            MyPanel.options = 3
            self.ids["physics_options"].text = "Physics mode selected : \n\n             No Physics"
        if instance.type == "Yes":
            MyPanel.cofac = True
            self.ids["cofactors_selection"].text = "Cofactors displayed : Yes"
        if instance.type == "No":
            MyPanel.cofac = False
            self.ids["cofactors_selection"].text = "Cofactors displayed : No"

    def select_options(self):
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


# define the object choice folder dialog
class DirectoryName(BoxLayout):
    cancel = ObjectProperty(None)

    def add_directory(self, inputname):
        valeur = self.ids[inputname].text
        if valeur != "":
            MyPanel.mainDirectory = valeur


# define the object settings dialog
class Parameters(BoxLayout):
    cancel = ObjectProperty(None)

    """check if the value in textinput is in the interval, if is true the value of the dictionnary parameter is replace,
    else the function alerts the user of his error"""

    def add_value(self, param, id):

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

            # replace the value in parameter with default values

    def reset(self):
        MyPanel.parametre.update(MyPanel.defaut)


class TI_meta(TextInput):

    def on_text(self, instance, value):
        meta_list = App.get_running_app().root.ids["Meta_list"]
        if meta_list.data:
            meta_list.data = [
                {"text": meta["id"], "root_widget": App.get_running_app().root.ids["Meta_list"]} for
                meta in MyPanel.graph.data["metabolites"] if
                value.upper() in meta["id"].upper()]
            if meta_list.opacity == 0:
                meta_list.opacity = 1


class TI_reac(TextInput):
    def on_text(self, instance, value):
        if App.get_running_app().root.ids["Reac_list"].data:
            App.get_running_app().root.ids["Reac_list"].data = [
                {"text": reac["id"], "root_widget": App.get_running_app().root.ids["Reac_list"]} for
                reac in MyPanel.graph.data["reactions"] if
                value.upper() in reac["id"].upper()]


class Compartment_buttons(Button):
    root_widget = ObjectProperty()

    def on_release(self):
        super().on_release()
        self.root_widget.btn_callback(self)


class Meta_list_buttons(Button):
    root_widget = ObjectProperty()

    def on_release(self, **kwargs):
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
        super().on_release()
        self.root_widget.btn_callback(self)


class Reac_List(RecycleView):
    def __init__(self, **kwargs):
        super(Reac_List, self).__init__(**kwargs)
        if MyPanel.graph.data:
            self.data = [{"text": reac["id"], 'root_widget': self} for reac in MyPanel.graph.data["reactions"]]

    def selected_keyword(self):
        message = f"Currently in search :\n\nMetabolites : {', '.join(MyPanel.graph.meta_keyword)}\n\nReactions : " \
                  f"{', '.join(MyPanel.graph.reac_keyword)}\n\nCompartments : {', '.join(MyPanel.graph.search_compartment)}"
        App.get_running_app().root.ids["keywords"].text = message

    def btn_callback(self, btn):
        if self.opacity == 1:
            MyPanel.graph.reac_keyword_update(btn.text)
            self.selected_keyword()


class Compartment_List(RecycleView):
    def __int__(self, **kwargs):
        super(Compartment_List, self).__init__(**kwargs)
        if MyPanel.graph.data:
            self.data = [{"text": comp["id"], 'root_widget': self} for comp in MyPanel.graph.data["compartment"]]

    def selected_keyword(self):
        message = f"Currently in search :\n\nMetabolites : {', '.join(MyPanel.graph.meta_keyword)}\n\nReactions : " \
                  f"{', '.join(MyPanel.graph.reac_keyword)}\n\nCompartments : {', '.join(MyPanel.graph.search_compartment)}"
        App.get_running_app().root.ids["keywords"].text = message

    def update_meta_list(self):
        temp_compartment = [Graph.cobra_compatibility(reac, False) for reac in MyPanel.graph.search_compartment]
        meta_list = App.get_running_app().root.ids["Meta_list"]
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
        if self.opacity == 1:
            MyPanel.graph.compartment_update(btn.text)
            self.selected_keyword()
            self.update_meta_list()


class plantGEMApp(App):

    def build(self):
        return MyPanel()
