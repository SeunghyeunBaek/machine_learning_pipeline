import pandas as pd

def drop_column(args: dict) -> dict:
    drop_column_list = ['Ticket', 'Cabin']
    args['df'] = args['df'].drop(drop_column_list, axis=1)

    return args


def extract_title(args: dict) -> dict:
    regex = r' ([A-Za-z]+)\.'
    args['df']['Title'] = args['df']['Name'].str.extract(regex, expand=False)

    return args


def replace_title(args: dict) -> dict:
    rare_title_list = ['Lady', 'Countess','Capt', 'Col',
                       'Don', 'Dr', 'Major', 'Rev', 'Sir',
                       'Jonkheer', 'Dona']
    miss_title_list = ['Mlle', 'Ms']

    args['df']['Title'] = args['df']['Title'].replace(rare_title_list, 'Rare')
    args['df']['Title'] = args['df']['Title'].replace(miss_title_list, 'Miss')
    args['df']['Title'] = args['df']['Title'].replace('Mme', 'Mrs')

    return args


def map_title(args: dict)-> dict:
    title_mapper_dict = {'Mr': 1, 'Miss': 2, 'Mrs': 3, 'Master': 4, 'Rare': 5}
    args['df']['Title'] = args['df']['Title'].map(title_mapper_dict)
    args['df']['Title'] = args['df']['Title'].fillna(0)

    return args


def convert_categorical_column(args: dict)-> dict:
    args['df']['Sex'] = args['df']['Sex'].map({'female': 1, 'male': 0}).astype(int)

    return args


def imputation(args: dict)-> dict:    
    pass