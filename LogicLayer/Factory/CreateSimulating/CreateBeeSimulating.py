from LogicLayer.Factory.CreateSimulating.ICreateSimulator import ICreateSimulator
from LogicLayer.Factory.Simulating.BeeSimulating import BeeSimulating
from LogicLayer import ImageMS

class CreateBeeSimulator(ICreateSimulator):

    def create_simulator(self, image_ms : ImageMS, bands_number : tuple = ()):
        return BeeSimulating(image_ms)
