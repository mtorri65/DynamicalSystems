from .simulation_model import Simulation, Simulation_Encoder, System


class Model:
    def __init__(self):
        self.simulation = Simulation()
        self.simulation_encoder = Simulation_Encoder()
        self.system = System()
