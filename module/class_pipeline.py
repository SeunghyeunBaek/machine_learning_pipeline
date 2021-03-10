from module.class_base import PipeLineBase, OperationBase
from collections.abc import Callable
from time import time
import logging


class Operation(OperationBase):


    def __init__(self, name: str,
                function: Callable,
                args: dict=dict(),
                description: str=""):
                
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
        self.operation_list = list()
        self.output_list = list()
        self.logger = None


    def set_logger(self, logger: logging.RootLogger):
        self.logger = logger


    def run(self):
        
        for i, operation in enumerate(self.operation_list):

            if i != 0:
                operation.set_args(self.output_list[i-1])
            
            start_time = time()
            operation.run()
            elapsed_time = round(time() - start_time, 3)
            msg = f"{i} Operation {operation.name} elapsed at {elapsed_time}s"

            if self.logger:
                self.logger.info(msg)

            else:
                print(msg)

            self.output_list.append(operation.output)


    def add_operation(self, operation:Operation):
        
        if type(operation) == list:
            self.operation_list += operation
            msg = f"Operation added: {[element.name for element in operation]}"

        else:    
            self.operation_list.append(operation)
            msg = f"Opeartion added {operation.name}"

        print(msg)


    def remove_operation(self, name: str):

        operation_name_list = [operation.name for operation in self.operation_list]
        
        if name in operation_name_list:
            self.operation_list = [operation for operation in self.operation_list if operation.name != name]
            msg = f"Operation {name} removed"

        else:
            msg = f"No operation {name} exists"

        print(msg)


    def show_operation(self, description=False):
        
        msg = f"Pipeline {self.name} operation list\n"

        if self.operation_list:

            for i, operation in enumerate(self.operation_list):

                if description:
                    msg += f"\t{i} {operation.name}\n\t\t{operation.description}\n"

                else:
                    msg += f"\t{i} {operation.name}\n"

        else:
            msg = f"No operation exists"

        print(msg)

    