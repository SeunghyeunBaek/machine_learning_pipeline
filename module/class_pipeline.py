"""Pipeline, Operator 클래스 정의 스크립트

    * Pipeline 클래스 정의
    * Operator 클래스 정의
    * 프로젝트에 따라 수정해서 사용

TODO:
    * Pipeline 분기 기능(merge) 추가
    * 예외처리 기능 추가
"""

from module.class_base import BasePipeline, BaseOperator
from collections.abc import Callable
from module.util import save_pickle
from copy import deepcopy
from time import time
import logging

class Operator(BaseOperator):

    """Operator 클래스 정의

    Pipeline 단위 실행 연산자 객체 클래스

    Attributes:
        name (str): 이름, 함수명으로 자동 설정
        description (str): 설명, 객체 생성 시 등록
        function (Callable): Operator가 실행할 함수
        args (str): 입력인자
        output (str): 출력인자 
    """

    def __init__(self, function: Callable, args: dict=dict(), description: str="")-> None:
        
        self.name = function.__name__
        self.description = description
        self.function = function
        self.args = args
        self.output = None


    def set_args(self, args: dict)-> None:
        """입력 인자 설정
        Args:
            args (dict): 입력인자
        """

        self.args = args


    def run(self)-> None:
        """Operator 실행
        """
        self.output = self.function(self.args)


class Pipeline(BasePipeline):

    """Pipeline 객체 클래스

    Attributes:
        name (str): 이름
        args (str): Pipeline 시작 시점의 입력 인자
        operator_list (list): Pipeline 에 등록한 Operator 객체 리스트
        output_list (list): Operator 가 실행될 때 마다 생성된 output 리스트
        logger (`logging.RootLogger`, optional): Pipeline 에 등록한 logger 
    """

    def __init__(self, name: str='pipeline', logger: logging.RootLogger=None)-> None:
        self.name = name
        self.args = dict()
        self.operator_list = list()
        self.output_list = list()
        self.logger = logger
        #TODO: Pipeline 병합 시 기록
        # self.merge_dict = {'pipeline': [self], 'name': [self.name]}


    def set_args(self, args: dict)-> None:
        """Pipeline 시작 시점의 입력 인자 설정
        
        Args:
            args(dict): 입력 인자
        """

        self.args = args

    #TODO: Depreceted, init 함수에 포함
    def set_logger(self, logger: logging.RootLogger)-> None:
        """Logger 객체 등록
        
        Args:
            logger(`logging.RootLogger`): logger 객체

        """

        self.logger = logger


    def run(self)-> None:
        """Pipeline 실행
            
            operator_list 내 모든 Operator 를 순차적으로 실행
            Operator 실행 후 생성된 output은 다음 Operator 의 args 로 입력
            모든 output 은 output_list 에 저장
            Opeartor 실행 시간 출력(logger 를 등록안하면 print 실행)

        """
        
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


    def add_operator(self, operator:Operator)-> None:
        """Operator 객체 등록

            Operator list, Operator 객체 모두 입력 가능

        Args:
            operator(Operator, list(Operator)): Operator 객체 또는 Operator 객체 list
        
        Examples:
            >> pipeline.add_operator([op1, op2, op3])
            >> pipeline.add_oeprator(op1)

        """
        
        if type(operator) == list:
            self.operator_list += operator
            msg = f"Operator added: {[element.name for element in operator]}"

        else:    
            self.operator_list.append(operator)
            msg = f"Opeartion added {operator.name}"

        print(msg)


    def remove_operator(self, name: str)-> None:
        """Pipeline 에서 Operator 삭제
            
            Opeartor 이름으로 삭제

        Args:
            name (str): Operator 이름
        
        Note:
            pipeline내 name 에 해당하는 operator 가 없으면 "No operator {name} exists" 출력

        """

        operator_name_list = [operator.name for operator in self.operator_list]
        
        if name in operator_name_list:
            self.operator_list = [operator for operator in self.operator_list if operator.name != name]
            msg = f"Operator {name} removed"

        else:
            msg = f"No operator {name} exists"

        print(msg)


    def show_operator(self, description=False)-> None:
        """Opeartor list 출력
            
            pipeline 에 등록한 operator 출력

        Args:
            description (bool, optional): Operator description 출력 여부

        Examples:
            >> pipeline.show_operator(description=True)
            >> Pipeline `preprocess` operator list
                0 `drop_column`
                        Drop Ticket, Carbin column
                1 `extract_title`
                        Extract title from Name column
                2 `replace_title`
                        Replace title(Rare, Miss, Mrs)
                3 `map_title`
                        Mapping title to integer
                4 `convert_categorical_column`
                        Convert female, male to 0, 1
                5 `impute_age`
                        Impute age as median for each sex, pclass
                6 `group_age`
                        Make age groups
                7 `make_new_feature`
                        Make FamilySize, IsAlone, AgePclass
                8 `convert_numeric_feature`
                        Group Fare
                9 `select_feature_ver1`
                        Select 8 feature
        """

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
    

    def save(self, path: str, clear_data=True)-> None:
        """Pipeline 저장

            Pipeline 객체를 pickle 형태로 저장

        Args:
            path (str): 저장 경로
            clear_data (bool, optional): False 로 설정시 output_list, args 모두 저장 

        """

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


    def save_data(self, path: str, final_only: bool=True)-> None:
        """pipeline 수행 후 데이터 저장

            output_list 를 pickle 형태로 저장

        Args:
            path (str): 데이터 저장 경로
            final_only (bool): True 로 설정 시 output_list 의 마지막 원소만 저장

        """

        #TODO 예외처리: output_list 에 원소가 없을 때
        data = self.output_list[-1] if final_only else self.output_list
        save_pickle(path, data)
        msg = f"Save data {path}"

        if self.logger:
            self.logger.info(msg)

        else:
            print(msg)

    #TODO: pipeline 병합 시 기록, show_merge_history 에서 확인
    def merge(self, pipeline, show_operator:bool=True)-> Pipeline:
        """두 Pipeline 연결

            두 pipeline 을 연결

            Args:
                pipeline (`Pipeline`): 뒤쪽에 연결하는 pipeline
                show_operator (bool, optional): True 로 설정 시 연결 후 operator_list 출력

            Returns:
                `Pipeline`: 연결한 pipeline

            Examples:
                >> merged_pipeline = front_pipeline.merge(pipeline=back_pipeline, show_operator=True)

        """
        
        front_pipeline = deepcopy(self)
        back_pipeline = pipeline

        front_pipeline.operator_list.extend(back_pipeline.operator_list)

        msg = f"Merge pipeline `{front_pipeline.name}`, {back_pipeline.name}"
        front_pipeline_operator_msg = front_pipeline.show_operator()
        back_pipeline_operator_msg = back_pipeline.show_operator()

        msg = msg + '\n' + f"`{front_pipeline.name}`"
        msg = msg + '\n' + front_pipeline_operator_msg
        msg = msg + '\n' + f"`<< {back_pipeline.name}`"
        msg = msg + '\n' + back_pipeline_operator_msg

        if self.logger:
            self.logger.info(msg)
        
        else:
            print(msg)
        
        return front_pipeline

    