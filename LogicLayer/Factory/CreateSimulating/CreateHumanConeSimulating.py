from LogicLayer.Factory.CreateSimulating.ICreateSimulator import ICreateSimulator
from LogicLayer.Factory.Simulating.HumanConeSimulating import HumanConeSimulating
from LogicLayer.ImageMS import ImageMS

class CreateHumanConeSimulator(ICreateSimulator):
    def create_simulator(self, image_ms: ImageMS, bands_number: tuple = ()):
        return HumanConeSimulating(image_ms) 