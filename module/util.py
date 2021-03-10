# import pandas_profiling
import pandas as pd
import logging
import yaml
import os


def load_yml(path):

    with open(path) as f:

        obj = yaml.load(f, Loader=yaml.FullLoader)

    return obj


# def get_eda_report(df:pd.DataFrame, path:str)-> None:
#     report = df.profile_report()
#     report.to_file(path)

#     return None


def set_logger(name: str, dir: str)-> logging.RootLogger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(os.path.join(dir, name+'.log'))

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger