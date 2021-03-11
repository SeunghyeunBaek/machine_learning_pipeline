from module.class_base import BasePipeline, BaseOperator
from collections.abc import Callable
from module.util import save_pickle
from copy import deepcopy
from time import time
import logging


class Operator(BaseOperator):


    def __init__(self, function: Callable, args: dict=dict(), description: str=""):
                
        self.function = function
        self.name = self.function.__name__
        self.args = args
        self.description = description
        self.output = None


    def set_args(self, args: dict):
        self.args = args


    def run(self):
        self.output = self.function(self.args)


class Pipeline(BasePipeline):


    def __init__(self, name: str='pipeline', logger: logging.RootLogger=None):
        self.name = name
        self.args = dict()
        self.operator_list = list()
        self.output_list = list()
        self.logger = logger
        #TODO: Pipeline 병합 시 기록
        # self.merge_dict = {'pipeline': [self], 'name': [self.name]}


    def set_args(self, args: dict):
        self.args = args

    #TODO: Depreceted, init 함수에 포함
    def set_logger(self, logger: logging.RootLogger):
        self.logger = logger


    def run(self):
        
        for i, operator in enumerate(self.operator_list):
            
            args = self.args if i == 0 else self.output_list[i-1]
            operator.set_args(args)

            # 실행 시간 출력
            start_time = time()
            operator.run()
            elapsed_time = round(time() - start_time, 3)
            msg = f"{i} operator {operator.name} elapsed at {elapsed_time} s"

            # Operator 내부 메시지를 설정했을 경우 내부 메시지 추가
            if operator.name in operator.output['log'].keys():
                operator_inner_msg = operator.output['log'][operator.name]
                msg = msg + '\n' + operator_inner_msg

            # Logger를 등록했다면 로깅
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
        
        msg = f"Pipeline `{self.name}` operator list\n"

        if self.operator_list:

            for i, operator in enumerate(self.operator_list):

                if description:
                    msg += f"\t{i} `{operator.name}`\n\t\t{operator.description}\n"

                else:
                    msg += f"\t{i} `{operator.name}`\n"

        else:
            msg = f"No operator exists"

        print(msg)
        
        return msg
    

    def save(self, path: str, clear_data=True):
        pipeline = deepcopy(self)

        if clear_data:
            pipeline.args = dict()
            pipeline.output_list = list()
        
        save_pickle(path, obj=pipeline)
        msg = f"Pipeline `{self.name}` saved {path}"

        if self.logger:
            self.logger.info(msg) 

        else:
            print(msg)

        del pipeline


    def save_data(self, path: str, final_only: bool=True):
        
        #TODO 예외처리: output_list 에 원소가 없을 때
        data = self.output_list[-1] if final_only else self.output_list
        save_pickle(path, self)
        msg = f"Save data {path}"

        if self.logger:
            self.logger.info(msg)

        else:
            print(msg)

    #TODO: pipeline 병합 시 기록, show_merge_history 에서 확인
    def merge(self, pipeline, show_operator:bool=True):
        # self.merge_dict['pipeline'].append(pipeline)
        # self.merge_dict['name'].append(pipeline.name)

        self.operator_list.extend(pipeline.operator_list)

        msg = f"Merge pipeline `{self.name}`, {pipeline.name}"
        front_pipeline_operator_msg = self.show_operator()
        back_pipeline_operator_msg = pipeline.show_operator()

        msg = msg + '\n' + f"`{self.name}`"
        msg = msg + '\n' + front_pipeline_operator_msg
        msg = msg + '\n' + f"`{pipeline.name}`"
        msg = msg + '\n' + back_pipeline_operator_msg

        if self.logger:
            self.logger.info(msg)
        
        else:
            print(msg)
        
        # print(self.operator_list)
        


    