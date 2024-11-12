from LogicLayer.Factory.CreateSimulating import ICreateSimulator
from LogicLayer.Factory.Simulating import DaltonianSimulating
from LogicLayer import ImageMS

class CreateDaltonianSimulator(ICreateSimulator):

    def create_simulator(self, image_ms : ImageMS, bands_number : tuple = ()):
        return DaltonianSimulating(image_ms)
