import unittest
import numpy as np
from LogicLayer.Simulations import Simulations

class TestSimulations(unittest.TestCase):
    """
    Test suite for the Simulations class.
    """
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.simulations = Simulations()
        # Create sample test data as lists instead of numpy arrays
        self.test_image_original = [[1, 2], [3, 4]]
        self.test_image_simulated = [[5, 6], [7, 8]]
        self.test_tuple = (self.test_image_original, self.test_image_simulated)
        
    def test_add_simulation(self):
        """Test adding a simulation to the historic"""
        # Test adding a new simulation
        self.simulations.add_simulation("test_sim", self.test_tuple)
        self.assertIn("test_sim", self.simulations.get_all_datas())
        
        # Test adding a duplicate simulation (should not add to the historic)
        self.simulations.add_simulation("test_sim", ([[1]], [[2]]))
        self.assertEqual(self.simulations.get_all_datas()["test_sim"], self.test_tuple)
        
    def test_delete_simulation(self):
        """Test deleting a simulation from the historic"""
        # Add a simulation first
        self.simulations.add_simulation("test_sim", self.test_tuple)
        
        # Test deleting existing simulation
        self.simulations.delete_simulation("test_sim")
        self.assertNotIn("test_sim", self.simulations.get_all_datas())
        
        # Test deleting non-existing simulation (should not raise error)
        self.simulations.delete_simulation("non_existing")
        
    def test_get_all_datas(self):
        """Test getting all simulations data"""
        # Test with empty historic
        self.assertEqual(len(self.simulations.get_all_datas()), 0)
        
        # Test with one simulation
        self.simulations.add_simulation("test_sim", self.test_tuple)
        datas = self.simulations.get_all_datas()
        self.assertEqual(len(datas), 1)
        self.assertEqual(datas["test_sim"], self.test_tuple)
        
    def test_get_data_by_array(self):
        """Test getting simulation data by array"""
        # Add test simulations with numpy arrays
        test_array1 = np.array([[5, 6], [7, 8]])
        test_array2 = np.array([[2, 3], [4, 5]])
        
        # Convert arrays to lists for comparison
        sim_tuple1 = (test_array1.tolist(), test_array1.tolist())
        sim_tuple2 = (test_array2.tolist(), test_array2.tolist())
        
        self.simulations.add_simulation("test_sim1", sim_tuple1)
        self.simulations.add_simulation("test_sim2", sim_tuple2)
        
        # Test getting data by simulated image array
        sim_name = self.simulations.__str__(test_array1.tolist())
        self.assertEqual(sim_name, "test_sim1")
        
        # Test with non-existing array
        non_existing = np.array([[99, 99], [99, 99]])
        sim_name = self.simulations.__str__(non_existing.tolist())
        self.assertIsNone(sim_name)

    def test_str(self):
        """Test string representation of simulation"""
        # Add a test simulation
        self.simulations.add_simulation("test_sim", self.test_tuple)
        
        # Test getting simulation name by array
        sim_data = self.simulations.get_data_by_key("test_sim")
        self.assertEqual(sim_data[0], "test_sim")
        self.assertEqual(sim_data[1], self.test_tuple)
        
        # Test with non-existing key
        with self.assertRaises(KeyError):
            self.simulations.get_data_by_key("non_existing")

if __name__ == '__main__':
    unittest.main() 