# import pandas_profiling
import pandas as pd
import pickle
import logging
import yaml
import os


def load_yml(path)-> dict:

    with open(path) as f:

        obj = yaml.load(f, Loader=yaml.FullLoader)

    return obj


def save_pickle(path, obj):

    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_pickle(path)-> object:

    with open(path, 'rb') as f:
        obj = pickle.load(f)
    
    return obj


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