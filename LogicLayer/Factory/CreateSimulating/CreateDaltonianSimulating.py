from LogicLayer.Factory.CreateSimulating.ICreateSimulator import ICreateSimulator
from LogicLayer.Factory.Simulating.DaltonianSimulating import DaltonianSimulating
from LogicLayer import ImageMS

class CreateDaltonianSimulator(ICreateSimulator):

    def create_simulator(self, image_ms : ImageMS, bands_number : tuple = (), **kwargs):
        return DaltonianSimulating(image_ms, kwargs.get('daltonian_type'))
