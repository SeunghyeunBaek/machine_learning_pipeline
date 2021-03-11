from itertools import product  # impute age
import pandas as pd


"""
def function_name(args: dict)-> dict
    ...

    return args
"""

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
    args['df']['Embarked'] = args['df']['Embarked'].fillna(args['df']['Embarked'].dropna().mode()[0])
    args['df']['Embarked'] = args['df']['Embarked'].map({'S': 0, 'C': 1, 'Q': 2}).astype(int)

    return args


def impute_age(args: dict)-> dict:
    sex_idx = [0, 1]
    pclass_idx = [1, 2, 3]
    msg = f"\tNumber of na Age row: {args['df']['Age'].isna().sum()}\n"

    for sex_id, pclass_id in product(sex_idx, pclass_idx):
        selected_age = args['df'].query(f"Sex=={sex_id} & Pclass=={pclass_id}")['Age'].dropna()
        guessed_age = selected_age.median()
        guessed_age = int(guessed_age/.5 + .5) * .5
        impute_condition = (args['df']['Age'].isna()) &\
                           (args['df']['Sex'] == sex_id) &\
                           (args['df']['Pclass'] == pclass_id)
        args['df'].loc[impute_condition, 'Age'] = guessed_age

        msg += f"\timpute age Sex: {sex_id} Pclass: {pclass_id} Age imputed as {guessed_age} {(impute_condition.sum())} rows\n"

    args['df']['Age'] = args['df']['Age'].astype('int')

    # log 의 key 는 반드시 함수명과 동일하게 설정
    args['log']['impute_age'] = msg

    return args


def group_age(args: dict)-> dict:
    args['df'].loc[(args['df']['Age'] <= 16), 'Age'] = 0
    args['df'].loc[(args['df']['Age'] > 16) & (args['df']['Age'] <= 32), 'Age'] = 1
    args['df'].loc[(args['df']['Age'] > 32) & (args['df']['Age'] <= 48), 'Age'] = 2
    args['df'].loc[(args['df']['Age'] > 48) & (args['df']['Age'] <= 64), 'Age'] = 3
    args['df'].loc[(args['df']['Age'] > 64), 'Age']

    return args


def make_new_feature(args: dict)-> dict:
    family_size = args['df']['SibSp'] + args['df']['Parch'] + 1
    is_alone = family_size.apply(lambda x: 1 if x == 1 else 0)
    age_pclass = args['df']['Age'] * args['df']['Pclass']

    args['df']['FamilySize'] = family_size
    args['df']['IsAlone'] = is_alone
    args['df']['AgePclass'] = age_pclass

    return args


def convert_numeric_feature(args: dict)-> dict:
    args['df']['Fare'].fillna(args['df']['Fare'].dropna().median(), inplace=True)
    args['df'].loc[ args['df']['Fare'] <= 7.91, 'Fare'] = 0
    args['df'].loc[(args['df']['Fare'] > 7.91) & (args['df']['Fare'] <= 14.454), 'Fare'] = 1
    args['df'].loc[(args['df']['Fare'] > 14.454) & (args['df']['Fare'] <= 31), 'Fare']   = 2
    args['df'].loc[ args['df']['Fare'] > 31, 'Fare'] = 3
    args['df']['Fare'] = args['df']['Fare'].astype(int)

    return args


def select_feature_ver1(args: dict)-> dict:

    feature_list = ['Sex','Title','Age','Embarked','IsAlone','Fare','AgePclass','Pclass']
    args['df'] = args['df'][feature_list]

    return args


def select_feature_ver2(args: dict)-> dict:

    feature_list = ['Sex','Title','Age','Embarked','IsAlone','Fare','AgePclass']
    args['df'] = args['df'][feature_list]

    return args