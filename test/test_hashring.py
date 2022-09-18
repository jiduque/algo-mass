import sys
import unittest

from io import StringIO

import dat_mass.hashring as hashring
import dat_mass._hashring.funcs as hr_funcs


class TestHashRing(unittest.TestCase):
    @staticmethod
    def main():
        num_nodes = 5
        hr = hashring.HashRing(num_nodes)

        nodes_to_add = [12, 18]
        hr.add_nodes(nodes_to_add)
        resources_to_add = [24, 21, 16, 23, 2, 29, 28, 7, 10]
        hr.add_resources(resources_to_add)
        hr.print()

        new_nodes = [5, 27, 30]
        hr.add_nodes(new_nodes)
        hr.print()

        hr.remove_node(12)
        hr.print()

    def test_e2e(self):
        expected_output = """Adding a head node 12 ...
Finger table for 12 is complete
Adding a node 18. Previous node is 12. Next node is 12.
Finger table for 12 is complete
Finger table for 18 is complete
Adding a resource 24
Adding a resource 21
Adding a resource 16
Adding a resource 23
Adding a resource 2
Adding a resource 29
Adding a resource 28
Adding a resource 7
Adding a resource 10
*****
Printing the hashring in clockwise order:
Node: 12,  Resources:  24 21 23 2 29 28 7 10  
Node: 18,  Resources:  16  
*****
Adding a node 5. Previous node is 18. Next node is 12.
Finger table for 5 is complete
Finger table for 12 is complete
Finger table for 18 is complete
Adding a node 27. Previous node is 18. Next node is 5.
Finger table for 5 is complete
Finger table for 12 is complete
Finger table for 18 is complete
Finger table for 27 is complete
Adding a node 30. Previous node is 27. Next node is 5.
Finger table for 5 is complete
Finger table for 12 is complete
Finger table for 18 is complete
Finger table for 27 is complete
Finger table for 30 is complete
*****
Printing the hashring in clockwise order:
Node: 5,  Resources:  2  
Node: 12,  Resources:  7 10  
Node: 18,  Resources:  16  
Node: 27,  Resources:  21 23 24  
Node: 30,  Resources:  28 29  
*****
Nothing to remove
*****
Printing the hashring in clockwise order:
Node: 5,  Resources:  2  
Node: 12,  Resources:  7 10  
Node: 18,  Resources:  16  
Node: 27,  Resources:  21 23 24  
Node: 30,  Resources:  28 29  
*****
"""
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        self.main()

        sys.stdout = old_stdout
        actual_output = captured_output.getvalue()
        captured_output.close()

        self.assertEqual(expected_output, actual_output)


class TestUnits(unittest.TestCase):
    def test_distance(self):
        k = 5
        inputs = [(29, 5), (29, 12), (5, 29)]
        expected_output = [8, 15, 24]
        for i in range(3):
            a, b = inputs[i]
            actual_output = hr_funcs.distance(k, a, b)
            self.assertEqual(expected_output[i], actual_output)


if __name__ == '__main__':
    unittest.main()
