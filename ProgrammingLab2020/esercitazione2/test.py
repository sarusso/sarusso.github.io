
from esame import Diff, ExamException

import unittest

score = 0

class TestAndGrade(unittest.TestCase):

    
    def test_correctness(self):
        
        diff = Diff()
        self.assertEqual(diff.compute([2,4,8,16]), [2,4,8])
        self.assertEqual(diff.compute([2,4,8,16,32]), [2,4,8,16])
        self.assertEqual(diff.compute([2,4,8,16,32,64]), [2,4,8,16,32])

        diff = Diff()
        self.assertEqual(diff.compute([2.5,4.5,10]), [2,5.5])
        
        diff = Diff(2)
        self.assertEqual(diff.compute([2,4,8,16,32,64]), [1,2,4,8,16])
        
        global score; score += 18 # Increase score  


    def test_correctness_edge_cases(self):
         
        diff = Diff()
        self.assertEqual(diff.compute([2,4]), [2])

        diff = Diff(3.7)
        diff_result = diff.compute([2,4,8,16])
        self.assertAlmostEqual(diff_result[0], 0.5405405405405405)
        self.assertAlmostEqual(diff_result[1], 1.081081081081081)
        self.assertAlmostEqual(diff_result[2], 2.162162162162162)
         
        global score; score += 2 # Increase score

    def test_correctness_interface(self):
         
        diff = Diff(ratio=2)
        self.assertEqual(diff.compute([2,4,8,16]), [1,2,4])

        global score; score += 2 # Increase score
 
 
    def test_init_type(self):
             
        with self.assertRaises(ExamException):
            Diff(None)            
        with self.assertRaises(ExamException):
            Diff('hi')
         
        global score; score += 1 # Increase score        
 
 
    def test_init_value_zero(self):
 
        with self.assertRaises(ExamException):
            Diff(0)
 
        global score; score += 1 # Increase score
 
 
    def test_init_value_negative(self):
 
        with self.assertRaises(ExamException):
            Diff(-1)

        global score; score += 1 # Increase score
 

    def test_input_type(self):
         
        diff = Diff(2)
        with self.assertRaises(ExamException):
            diff.compute(None)
 
        with self.assertRaises(ExamException):
            diff.compute(1)
 
        global score; score += 2 # Increase score
 
 
    def test_input_value(self):
         
        diff = Diff()
        with self.assertRaises(ExamException):
            diff.compute([2])
 
        global score; score += 2 # Increase score
 
 
    def test_input_data_items(self):
         
        diff = Diff(2)
        with self.assertRaises(ExamException):
            diff.compute([1,3,'ciao', 5])
 
        global score; score += 1 # Increase score
 
 
 
    # Print the score
    @classmethod
    def tearDownClass(cls):
        global score
        print('\n\n-------------')
        print('| Voto: {}  |'.format(score))
        print('-------------\n')


# Run the tests
unittest.main()

