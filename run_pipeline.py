"""Pipeline 실행

    * make_pipeline.py 에서 생성한 pipeline 실행
    * 전처리 데이터 저장 

Examples:
    >> import pandas as pd
    >> import pickle
    >> with open("preprocess_pipeline.pkl", 'rb') as f:
            pipeline = pickle.load(f)
    >> df = pd.read_csv('data.csv')
    >> pipeline.set_args({'df': df, 'log':dict()})
    >> pipeline.run()
    >> pipeline.save_data("preprocessed_data.pkl")

TODO:
    * 전처리 데이터 저장 경로 구조 설계

"""

from module.util import load_yml, set_logger  # util
from module.util import load_pickle
import pandas as pd
import os

PRJ_DIR = os.path.dirname(__file__)
PROCESSED_DATA_DIR = os.path.join(PRJ_DIR, 'output/data/')
CONFIG_PATH = os.path.join(PRJ_DIR, 'config/config.yml')
PIPELINE_PATH = os.path.join(PRJ_DIR, 'output/pipeline/preprocess_pipeline.pkl')

config_dict = load_yml(CONFIG_PATH)
logger = set_logger(name='run_pipeline', dir=config_dict['dir']['log'])

if __name__ == '__main__':

    df = pd.read_csv(config_dict['path']['train_data'])
    logger.info(f"Load data train: {df.shape}")

    # pipeline 불러오기
    pipeline = load_pickle(PIPELINE_PATH)
    pipeline.set_logger(logger=logger)
    pipeline.set_args(args={'df': df, 'log': dict()})  # 입력 데이터 설정

    # pipeline 실행
    pipeline.run()

    # 전처리 데이터 저장
    pipeline.save_data(path=os.path.join(PROCESSED_DATA_DIR,
                                         'train_processed_data.pkl'))