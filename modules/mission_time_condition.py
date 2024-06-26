"""
Checks whether the drone has reached its max flight time and sends it back to launch.
"""

import time

from . import condition


class MissionTimeCondition(condition.Condition):
    """
    Checks if drone exceeds the maximum flight time limit, inherits from Evaluate class
    """

    __create_key = object()

    @classmethod
    def create(
        cls, start_time: "float | None", maximum_flight_time: "float | None"
    ) -> "tuple[bool, MissionTimeCondition | None]":
        """
        start_time: float
            The time the drone started the mission in seconds.
         maximum_flight_time: float
            Max flight time for drone in seconds.
        """
        if start_time is None:
            return False, None

        if maximum_flight_time is None:
            return False, None

        return True, MissionTimeCondition(cls.__create_key, start_time, maximum_flight_time)

    def __init__(
        self, class_private_create_key: object, start_time: float, maximum_flight_time: float
    ) -> None:
        """
        Private constructor, use create() method
        """
        assert class_private_create_key is MissionTimeCondition.__create_key
        self.start_time = start_time
        self.maximum_flight_time = maximum_flight_time
        self.lap_time = 0
        self.previous_time_elapsed = -1

    def evaluate_condition(self) -> bool:
        """
        Evaluates whether the drone should land based on time remaining.
        """
        current_time = time.time()
        if (current_time + self.lap_time) - self.start_time < self.maximum_flight_time:
            return False

        return True

    def output_time_elapsed(self, frequency: int) -> None:
        """
        Outputs the total time elapsed during the mission.
        frequency: int
            Frequency to print time elapsed to the console.
        """
        time_elapsed = int(time.time() - self.start_time)

        if time_elapsed % frequency == 0 and time_elapsed != self.previous_time_elapsed:
            self.previous_time_elapsed = time_elapsed
            print(f"Elapsed time (s): {time_elapsed}")

    def update_lap_time(self, lap_time: float) -> None:
        """
        Updates the time taken to fly one lap.
        """
        self.lap_time = lap_time

    def message(self) -> None:
        """
        Outputs status when the drone has exceeded the time limit.
        """
        current_time = time.time()

        print("\n###########################################################")
        print("This mission has exceeded the maximum flight time limit.")
        print(f"Specified maximum flight time limit: {self.maximum_flight_time}")
        print(f"Mission start time: {self.start_time}")
        print(f"Time when condition was met: {current_time}")
        print(f"Total flight time: {current_time - self.start_time}")
        print(f"Time of previous lap: {self.lap_time}")
        print(
            f"Total flight time + time to fly another lap: {(current_time - self.start_time) + self.lap_time}"
        )
        print("###########################################################\n")
