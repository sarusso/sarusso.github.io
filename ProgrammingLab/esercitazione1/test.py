
from esame import MovingAverage, ExamException

import unittest

score = 0

class TestAndGrade(unittest.TestCase):

    def test_correctness(self):
        
        moving_average = MovingAverage(2)
        self.assertEqual(moving_average.compute([2,4,8,16]), [3,6,12])
        self.assertEqual(moving_average.compute([2,4,8,16,32]), [3,6,12,24])
        self.assertEqual(moving_average.compute([2,4,8,16,32,64]), [3,6,12,24,48])

        moving_average = MovingAverage(3)
        self.assertEqual(moving_average.compute([3,6,9,12]), [6,9])

        moving_average = MovingAverage(4)
        self.assertEqual(moving_average.compute([2,4,8,16,32]), [7.5,15])
        
        global score; score += 18 # Increase score  


    def test_correctness_edge_cases(self):
        
        moving_average = MovingAverage(1)
        self.assertEqual(moving_average.compute([2,4,8,16]), [2,4,8,16])
        self.assertEqual(moving_average.compute([2]), [2])

        moving_average = MovingAverage(4)
        self.assertEqual(moving_average.compute([2,4,8,16]), [7.5])
        
        global score; score += 2 # Increase score


    def test_init_type(self):
            
        with self.assertRaises(ExamException):
            MovingAverage(None)            
        with self.assertRaises(ExamException):
            MovingAverage('hi')
        
        global score; score += 2 # Increase score        


    def test_init_value_zero(self):

        with self.assertRaises(ExamException):
            MovingAverage(0)

        global score; score += 1 # Increase score


    def test_init_value_negative(self):

        with self.assertRaises(ExamException):
            MovingAverage(-1)


    def test_init_value_float(self):

        with self.assertRaises(ExamException):
            MovingAverage(5.7)
        
        global score; score += 1 # Increase score


    def test_input_type(self):
        
        moving_average = MovingAverage(2)
        with self.assertRaises(ExamException):
            moving_average.compute(None)

        with self.assertRaises(ExamException):
            moving_average.compute(1)

        global score; score += 2 # Increase score


    def test_input_value(self):
        
        moving_average = MovingAverage(3)
        with self.assertRaises(ExamException):
            moving_average.compute([2,4])

        global score; score += 2 # Increase score


    def test_input_data_items(self):
        
        moving_average = MovingAverage(2)
        with self.assertRaises(ExamException):
            moving_average.compute([1,3,'ciao', 5])

        global score; score += 2 # Increase score



    # Print the score
    @classmethod
    def tearDownClass(cls):
        global score
        print('\n\n-------------')
        print('| Voto: {}  |'.format(score))
        print('-------------\n')


# Run the tests
unittest.main()
