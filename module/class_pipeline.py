from module.class_base import PipeLineBase, OperatorBase
from collections.abc import Callable
from time import time
import logging


class Operator(OperatorBase):


    def __init__(self, name: str, function: Callable, args: dict=dict(), description: str=""):
                
        self.name = name
        self.function = function
        self.args = args
        self.description = description
        self.output = None


    def set_args(self, args: dict):
        self.args = args


    def run(self):
        self.output = self.function(self.args)


class PipeLine(PipeLineBase):


    def __init__(self, name: str='pipeline'):
        self.name = name
        self.operator_list = list()
        self.output_list = list()
        self.logger = None


    def set_logger(self, logger: logging.RootLogger):
        self.logger = logger


    def run(self):
        
        for i, operator in enumerate(self.operator_list):

            if i != 0:
                operator.set_args(self.output_list[i-1])
            
            start_time = time()
            operator.run()
            elapsed_time = round(time() - start_time, 3)
            msg = f"{i} operator {operator.name} elapsed at {elapsed_time}s"

            if self.logger:
                self.logger.info(msg)

            else:
                print(msg)

            self.output_list.append(operator.output)


    def add_operator(self, operator:Operator):
        
        if type(operator) == list:
            self.operator_list += operator
            msg = f"Operator added: {[element.name for element in operator]}"

        else:    
            self.operator_list.append(operator)
            msg = f"Opeartion added {operator.name}"

        print(msg)


    def remove_operator(self, name: str):

        operator_name_list = [operator.name for operator in self.operator_list]
        
        if name in operator_name_list:
            self.operator_list = [operator for operator in self.operator_list if operator.name != name]
            msg = f"Operator {name} removed"

        else:
            msg = f"No operator {name} exists"

        print(msg)


    def show_operator(self, description=False):
        
        msg = f"Pipeline {self.name} operator list\n"

        if self.operator_list:

            for i, operator in enumerate(self.operator_list):

                if description:
                    msg += f"\t{i} {operator.name}\n\t\t{operator.description}\n"

                else:
                    msg += f"\t{i} {operator.name}\n"

        else:
            msg = f"No operator exists"

        print(msg)
    