from LogicLayer.Factory.CreateSimulating import ICreateSimulator
from LogicLayer.Factory.Simulating import BeeSimulating
from LogicLayer import ImageMS

class CreateBeeSimulator(ICreateSimulator):

    def create_simulator(self, image_ms : ImageMS, bands_number : tuple = ()):
        return BeeSimulating(image_ms)
