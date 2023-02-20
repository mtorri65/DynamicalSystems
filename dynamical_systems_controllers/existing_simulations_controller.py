import tkinter as tk

from models.main_model import Model
from models.auth_model import User
from views.main import View


class ExistingSimulationsController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["existing_simulations"]
#        self.selection = self.model.system.selected_system
        self._bind()

    def _bind(self) -> None:
#        """Binds controller functions with respective buttons in the view"""
#        self.frame.signup_btn.config(command=self.switch_system_characteristics)
        self.frame.simulations_listbox.bind("<<ListboxSelect>>", self._select_item)
        self.frame.previous_button.config(command=self.switch_start)

    def update_view(self):
        selected_system = self.model.system.selected_system
        self.frame.mechanical_system_label.config(text=selected_system.replace('_',' '))

    def _update_list_of_systems(self):
        self.view.frames["start"].mechanical_systems_listbox.delete(0,tk.END)        
        systems_list = self.model.system.get_list_of_systems()
        for system in systems_list:
            self.view.frames["start"].mechanical_systems_listbox.insert('end', system)

    def switch_start(self) -> None:
        self._update_list_of_systems()
        self.view.switch('start', '')


    def _select_item(self, event):
#        self.open_button['state'] = tk.ACTIVE
#        global selected_system
#        global selected_simulation

        self.selection = event.widget.curselection()
        if self.selection:
            index = self.selection[0]
            selected_simulation = event.widget.get(index)    
 #           simulations_window_handle = win32gui.FindWindow(None, title + ' - existing simulations')
 #           simulations_window_rect   = win32gui.GetWindowRect(simulations_window_handle)
            self.view.switch("system_characteristics", 'system description')


    def switch_system_characteristics(self) -> None:
        self.view.switch("system_characteristics")

    def signin(self) -> None:
        username = self.frame.username_input.get()
        pasword = self.frame.password_input.get()
        data = {"username": username, "password": pasword}
        print(data)
        self.frame.password_input.delete(0, last=len(pasword))
        user: User = {"username": data["username"]}
        self.model.auth.login(user)