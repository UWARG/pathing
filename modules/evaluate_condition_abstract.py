"""
Abstract base class for evaluating drone conditions
"""
import abc


class EvaluateCondition(abc.ABC):
    """
    Wrapper for different classes to check conditions
    """
    @abc.abstractmethod
    def evaluate(self) -> bool:
        """
        The appropriate evaluate method depending on the child
        """

    @abc.abstractmethod
    def message(self):
        """
        A message to output when the condition evalues to true
        """
