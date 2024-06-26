"""
Module to evaluate multiple Evaluator objects
"""

from . import condition


class ConditionEvaluator:
    """
    Attributes:
        condition_list : A list of EvaluateCondition objects, representing all the
        conditions to evaluate
    """

    def __init__(self, condition_list: "list[condition.Condition]") -> None:
        """
        Constructor

        Parameters:
            condition_list : A list of EvaluateCondition objects, representing conditions
            to evaluate
        """
        self.evaluate_object_list = condition_list

    def evaluate_all_conditions(self) -> bool:
        """
        Runs all the evaluate objects. If any of the evaluations return true, evaluate_all outputs
        status messages to the console and returns true.
        """
        evaluation = False
        for evaluate_object in self.evaluate_object_list:
            if evaluate_object.evaluate_condition():
                evaluation = True
                evaluate_object.message()

        return evaluation
