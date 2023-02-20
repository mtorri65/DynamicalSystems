from .simulation_model import Simulation, Simulation_Encoder, System


class Model:
    def __init__(self):
        self.simulation = Simulation()
        self.simulation_encoder = Simulation_Encoder()
        self.system = System()

    def printMessage_Start(self):
        print('Hello from the Start!')

    def printMessage_SystemCharacteristics(self):
        print('Hello from the System Characteristics!')

    def printMessage_ExistingSimulations(self):
        print('Hello from the Existing Simulations!')
