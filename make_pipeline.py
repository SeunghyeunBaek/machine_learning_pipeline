from module.class_pipeline import Pipeline, Operator  # class 정의
from module.util import load_yml, set_logger  # util
from module.func_operator import *  # opeartion 함수 정의
from copy import deepcopy
import pandas as pd
import os

PRJ_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(PRJ_DIR, 'config/config.yml')
PIPELINE_DIR = os.path.join(PRJ_DIR, 'output/pipeline/')

config_dict = load_yml(CONFIG_PATH)
logger = set_logger(name='make_preprocess_pipeline', dir=config_dict['dir']['log'])


if __name__ == '__main__': 

    # pipeline 선언
    preprocess_pipe = Pipeline(name='preprocess', logger=logger)  # pipeline 객체 생성

    # operator 객체 생성
    drop_column_op = Operator(function=drop_column,
                              description="Drop Ticket, Carbin column")

    extract_title_op = Operator(function=extract_title,
                                description="Extract title from Name column")

    replace_title_op = Operator(function=replace_title,
                                description='Replace title(Rare, Miss, Mrs)')

    map_title_op = Operator(function=map_title,
                            description='Mapping title to integer')
    
    convert_categorical_column_op = Operator(function=convert_categorical_column,
                                             description='Convert female, male to 0, 1')

    impute_age_op = Operator(function=impute_age,
                             description='Impute age as median for each sex, pclass')
    
    group_age_op = Operator(function=group_age,
                            description='Make age groups')

    make_new_feature_op = Operator(function=make_new_feature,
                                   description='Make FamilySize, IsAlone, AgePclass')                            

    convert_numeric_feature_op = Operator(function=convert_numeric_feature,
                                          description='Group Fare')

    select_feature_op = Operator(function=select_feature_ver1,
                                 description='Select 8 feature')

    # pipeline에 operator 등록
    operator_list = [drop_column_op,
                    extract_title_op, 
                    replace_title_op,
                    map_title_op, 
                    convert_categorical_column_op,
                    impute_age_op,
                    group_age_op,
                    make_new_feature_op,
                    convert_numeric_feature_op,
                    select_feature_op]

    preprocess_pipe.add_operator(operator_list)

    # pipeline operator 조회
    msg = preprocess_pipe.show_operator(description=True)
    logger.info(f"Operator list\n{msg}")

    # pipeline 저장
    preprocess_pipe.save(path=os.path.join(PIPELINE_DIR, 'preprocess_pipeline.pkl'))

    # TODO: pipeline 분기 설정