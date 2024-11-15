from LogicLayer.Factory.CreateSimulating.ICreateSimulator import ICreateSimulator
from LogicLayer.Factory.Simulating.HumanSimulating import HumanSimulating
from LogicLayer import ImageMS

class CreateHumanSimulator(ICreateSimulator):
    def create_simulator(self, image_ms : ImageMS, bands_number : tuple = ()):
        return HumanSimulating(image_ms)