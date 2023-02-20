import tkinter as tk

from dynamical_systems_models.main_model import Model
from dynamical_systems_views.main_view import View


class StartController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["start"]
        self._bind()

#        self._update_list_of_systems()

    def _bind(self) -> None:
#        self.frame.signout_btn.config(command=self.logout)
        self.frame.new_button.config(command=self.switch_system_characteristics)
        self.frame.mechanical_systems_listbox.bind("<<ListboxSelect>>", self._select_system)
#        self.frame.bind("<<ShowFrame>>", self._update_list_of_systems)

    def _select_system(self, event):
#        self.open_button['state'] = tk.ACTIVE
        system = event.widget.curselection()
        if system:
            index = system[0]
            selected_system = event.widget.get(index)    
            self.model.system.selected_system = selected_system
            self.view.frames['existing_simulations'].simulations_listbox.delete(0, tk.END)        
            self.switch_existing_simulations(selected_system)

    def _update_list_of_simulations(self, selected_system):
        selected_system_simulations = self.model.system.get_list_of_simulations(selected_system)
        for simulation in selected_system_simulations:
            self.view.frames['existing_simulations'].simulations_listbox.insert('end', simulation)

    def _update_mechanical_system_label(self, system):
        self.view.frames['existing_simulations'].mechanical_system_label.config(text = system)

    def switch_system_characteristics(self) -> None:
        self.view.switch("system_characteristics", 'system description')

    def switch_existing_simulations(self, selected_system) -> None:
        self._update_list_of_simulations(selected_system)
        self._update_mechanical_system_label(selected_system)        
        self.view.switch('existing_simulations', 'existing simulations')

    def update_view(self) -> None:
        current_user = self.model.auth.current_user
        if current_user:
            username = current_user["username"]
            self.frame.greeting.config(text=f"Welcome, {username}!")
        else:
            self.frame.greeting.config(text=f"")