from module.class_pipeline import PipeLine, Operator  # class 정의
from module.util import load_yml, set_logger  # util
from module.func_operator import *  # opeartion 함수 정의
import pandas as pd
import os

PRJ_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(PRJ_DIR, 'config/config.yml')
PIPELINE_DIR = os.path.join(PRJ_DIR, 'pipeline/')
PROCESSED_DATA_DIR = os.path.join(PRJ_DIR, 'output/')

config_dict = load_yml(CONFIG_PATH)
logger = set_logger(name='train_process', dir=config_dict['dir']['log'])


if __name__ == '__main__': 

    # 데이터 불러오기
    df = pd.read_csv(config_dict['path']['train_data'])
    logger.info(f"Load data train: {df.shape}")

    # pipeline 선언
    pipeline = PipeLine(name='train_process')  # pipeline 객체 생성
    pipeline.set_args(args={'df': df, 'log': dict()})  # Input 설정  
    pipeline.set_logger(logger)  # logger 설정

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
                                          
    # pipeline에 operator 등록
    operator_list = [drop_column_op,
                    extract_title_op, 
                    replace_title_op,
                    map_title_op, 
                    convert_categorical_column_op,
                    impute_age_op,
                    group_age_op,
                    make_new_feature_op,
                    convert_numeric_feature_op]
    pipeline.add_operator(operator_list)

    # pipeline operator 조회
    msg = pipeline.show_operator(description=True)
    logger.info(f"Operator list\n{msg}")

    # pipeline 실행
    pipeline.run()

    # 최종 데이터만 저장
    pipeline.dump(path=os.path.join(PROCESSED_DATA_DIR, 'train_processed.pkl'),
                  data_only=True)

    # pipeline 저장
    pipeline.dump(path=os.path.join(PIPELINE_DIR, "preprocess.pkl"),
                  data_only=False,
                  initiate_data=True)
