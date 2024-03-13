"""
Module to evaluate multiple Evaluator objects to determine if drone should RTL
"""

from . import evaluate_condition_abstract


class MultipleEvaluator():
    """
    Attributes: 
        evaluate_object_list : A list of EvaluateCondition objects, representing conditions 
        to evaluate when determining RTL
    """
    def __init__(self,
                 evaluate_object_list : list["evaluate_condition_abstract.EvaluateCondition"]):
        """
        Constructor

        Parameters: 
            evaluate_object_list : A list of EvaluateCondition objects, representing conditions 
            to evaluate when determining RTL
        """
        self.evaluate_object_list = evaluate_object_list


    def evaluate_all(self) -> bool:
        """
        Runs all the evaluate objects. If any of the evaluations return true, evaluate_all outputs
        a message to the console and returns true, signifying that the drone should RTL.
        """
        evaluation = False
        for evaluate_object in self.evaluate_object_list:
            if evaluate_object.evaluate():
                evaluation = True
                evaluate_object.message()

        return evaluation
    