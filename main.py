from module.class_pipeline import PipeLine, Operator  # class 정의
from module.util import load_yml, set_logger  # util
from module.func_operator import *  # opeartion 함수 정의

import pandas as pd
import os

PRJ_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(PRJ_DIR, 'config/config.yml')

config_dict = load_yml(CONFIG_PATH)
logger = set_logger(name='process', dir=config_dict['dir']['log'])


if __name__ == '__main__': 

    # 데이터 불러오기
    train_df = pd.read_csv(config_dict['path']['train_data'])
    test_df = pd.read_csv(config_dict['path']['test_data'])
    merge_df = pd.concat([train_df, test_df], axis=0)
    logger.info(f"Load data train: {train_df.shape} test: {test_df.shape}")

    #get_eda_report(df=merge_df, path=config_dict['path']['eda_report'])
    logger.info(f"Save eda report {config_dict['path']['eda_report']}")

    # pipeline 선언
    args = {'df': merge_df}  # 초기 입력값
    pipeline = PipeLine(name='preprocess', args=args)  # pipeline 객체 생성  
    pipeline.set_logger(logger)  # logger 정의

    """
    1. Drop columns v
    2. Extract titles v
    3. Replace titles v
    4. Map titles v
    5. Convert categorical features v
    6. Impute age
    7. Group age
    8. Family size
    """

    # operator 객체 생성
    drop_column_op = Operator(name='drop_column',
                               function=drop_column,
                               description="Drop Ticket, Carbin column")

    extract_title_op = Operator(name='extract_title',
                                 function=extract_title,
                                 description="Extract title from Name column")

    replace_title_op = Operator(name='replace_title',
                                 function=replace_title,
                                 description='Replace title(Rare, Miss, Mrs)')

    map_title_op = Operator(name='map_title',
                             function=map_title,
                             description='Mapping title to integer')
    
    convert_categorical_column_op = Operator(name='convert_categorical_feature',
                                              function=convert_categorical_column,
                                              description='convert female, male to 0, 1')

    # pipeline 에 operator 등록
    operator_list = [drop_column_op,
                    extract_title_op, 
                    replace_title_op,
                    map_title_op, 
                    convert_categorical_column_op]

    pipeline.add_operator(operator_list)

    # pipline operator 조회
    pipeline.show_operator(description=True)

    # pipeline 실행
    pipeline.run()