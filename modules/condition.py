"""
Abstract class for evaluating drone conditions
"""

import abc


class Condition(abc.ABC):
    """
    Wrapper for different classes to check conditions
    """

    @abc.abstractmethod
    def evaluate_condition(self) -> bool:
        """
        The appropriate evaluate method depending on the child
        """

    @abc.abstractmethod
    def message(self) -> None:
        """
        A message to output when the condition evalues to true
        """
