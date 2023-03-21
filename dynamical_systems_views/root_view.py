from tkinter import Tk
from tkinter import font as tkfont

from . import views_constants as vc

# globals
#font = 'Helvetica, '
#root_folder_path = os.getcwd() + '\\'
#mechanical_system_library_path = root_folder_path + 'Mechanical_Systems_Library\\'
#mechanical_system_path = ''
#mechanical_system_simulation_path = ''
#title = 'Dynamical Systems'
#icon = 'images\\Chaos.ico'
#offset_x = 50
#offset_y = 50
#selected_simulation = ''
#simulation = simulator_engine.Simulation()
#simulation_serialized = {}

class Root(Tk):
    def __init__(self):
        super().__init__()
        self._frame = None
        self.title(vc.title)
        self.iconbitmap(vc.icon)
        self.geometry('+' + str(vc.offset_x) + '+' + str(vc.offset_y))
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight='bold', slant='italic')
