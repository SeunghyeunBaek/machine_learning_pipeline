from module.util import load_yml, set_logger  # util
from module.util import load_pickle
import pandas as pd
import os

PRJ_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(PRJ_DIR, 'config/config.yml')
PIPELINE_PATH = os.path.join(PRJ_DIR, 'output/preprocess.pkl')
PROCESSED_DATA_DIR = os.path.join(PRJ_DIR, 'output/')

config_dict = load_yml(CONFIG_PATH)
logger = set_logger(name='test_process', dir=config_dict['dir']['log'])

if __name__ == '__main__':

    df = pd.read_csv(config_dict['path']['test_data'])
    logger.info(f"Load data test: {df.shape}")

    # pipeline 불러오기
    pipeline = load_pickle(PIPELINE_PATH)
    pipeline.set_args(args={'df': df, 'log': dict()})
    pipeline.set_logger(logger=logger)
    
    # pipeline 실행
    pipeline.run()

    # 전처리 데이터 저장
    pipeline.dump(path=os.path.join(PROCESSED_DATA_DIR, 'test_processed.pkl'),
                  data_only=True)