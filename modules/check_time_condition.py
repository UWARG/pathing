"""
Checks whether the drone has reached its max flight time and sends it back to launch.
"""
import time

from . import evaluate_condition_abstract


class CheckTimeCondition(evaluate_condition_abstract.EvaluateCondition):
    """
    Checks if drone exceeds the maximum flight time limit, inherits from Evaluate class
    """
    def __init__(self, start_time : float, maximum_flight_time: float):
        """
        Constructor
        start_time: float
            The time the drone started the mission in seconds.
         maximum_flight_time: float
            Max flight time for drone in seconds.
        """
        self.start_time = start_time
        self.maximum_flight_time = maximum_flight_time


    def evaluate(self) -> bool:
        """
        Evaluates whether the drone should land based on time remaining
        """
        current_time = time.time()
        if current_time - self.start_time < self.maximum_flight_time:
            return False
        else:
            return True


    def output_time_elapsed(self):
        """
        Outputs the total time elapsed during the mission
        """
        current_time =time.time()
        print(f"Elapsed time (s): {current_time - self.start_time}")


    def message(self):
        """
        Outputs status when the drone has exceeded the time limit
        """
        print("Exceeded flight time limit")
        