import unittest
from unittest import mock
import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from checkers.timers import GameTimer, PlayerTimer

class TestTimer(unittest.TestCase):
    # initilizies the pygame module before running it    
    def setUp(self):
        pygame.init()

    # initializes the pygame timer and tests the GameTimer class 
    # to see if it is working correctly
    #TESTS THE TIMER INITIALIZATION AND FORMAT
    def test_01_game_timer_initialization(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 1: Game Timer Initialization')
        
        with mock.patch('pygame.time.get_ticks', return_value=0): # mocking the inbuilt 
            # pygame timer to return 0 so that we can test the initialization
            # YES YOU COULD MOCK IT TO RETURN ANYTHING!
            # ALSO IT IS BETTER TO
            # MOCK IT TO RETURN 0 SO THAT WE CAN TEST THE INITIALIZATION
            timer = GameTimer()
            
        print(f'Timer start time: {timer.start_time}')
        print(f'Expected start time: 0')
        
        try:
            self.assertEqual(timer.start_time, 0)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')

    # tests the GameTimer class to see if the format_time is properly formatting
    # in {hrs}:{mins}:{secs} format    
    def test_02_game_timer_format(self): 
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 2: Game Timer Format')
       # we are mocking the pygame timer two times here since 
       # the first call in __init__ sets start_time to 0 
       # then the second call should set the passed time 
       # time in milliseconds and this sets us up to change the 
        with mock.patch('pygame.time.get_ticks') as mock_time:
            # first call in _init__ sets start_time to 0
            mock_time.return_value = 0
            timer = GameTimer()
            
            # Second call in get_time() should return 3660000 (1hr, 1min in ms)
            mock_time.return_value = 3660000
            formatted_time = timer.format_time()
            
        print(f'Formatted time: {formatted_time}')
        print(f'Expected format: 01:01:00') 
        
        try:
            self.assertEqual(formatted_time, "01:01:00")
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
    # tests the PlayerTimer class to see if it is properly initialized
    # and if it is working correctly
    def test_03_player_timer_initialization(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 3: Player Timer Initialization')
        
        timer = PlayerTimer(initial_time=300)  # 5 minutes
        
        print(f'Initial time: {timer.time_left}')
        print(f'Timer active: {timer.is_active}')
        print(f'Expected time: 300')
        print(f'Expected active: False')
        
        try:
            self.assertEqual(timer.time_left, 300)
            self.assertFalse(timer.is_active)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')

    # tests the PlayerTimer class to see if it is properly updating the time
    # and if it is working correctly
    # it updates the time by 5 seconds and checks if it is working correctly
    # this is used for the countdown
    def test_04_player_timer_update(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 4: Player Timer Update')
        
        timer = PlayerTimer(initial_time=300)  # 5 minutes
        timer.is_active = True # the timer is active and is going down
        timer.update(5)  # Update by 5 seconds
        
        print(f'Time left after 5 second update: {timer.time_left}')
        print(f'Expected time left: 295')
        
        try:
            self.assertEqual(timer.time_left, 295)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')

    # tests the PlayerTimer class to see if it is properly formatting the time
    # this time in {mins}:{secs} format
    def test_05_player_timer_format(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 5: Player Timer Format')
        
        timer = PlayerTimer(initial_time=65)  # 1 minute 5 seconds
        formatted_time = timer.format_time() # formatting it
        
        print(f'Formatted time: {formatted_time}')
        print(f'Expected format: 01:05')
        
        try:
            self.assertEqual(formatted_time, "01:05")
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')

    # tests the PlayerTimer class to see if it is properly 
    # checking if the timer is expired
    # used in losing or winning or paused situations
    def test_06_player_timer_expiration(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 6: Player Timer Expiration')
        
        timer = PlayerTimer(initial_time=2) # 2 seconds
        timer.is_active = True
        timer.update(3)  # Update more than the initial time
        
        print(f'Time left: {timer.time_left}')
        print(f'Is timer expired: {timer.is_expired()}')
        print(f'Expected expired: True')
        
        try:
            self.assertTrue(timer.is_expired())
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')


if __name__ == '__main__':
    unittest.main()