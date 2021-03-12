from model.architecture import TorchNN
from torch.autograd import Variable
import torch

from module.util import load_yml, load_pickle
import numpy as np

if __name__ == '__main__':

    DATA_PATH = '/workspace/pipeline/output/data/train_processed_data.pkl'
    CONFIG_PATH = '/workspace/pipeline/config/train_config.yml'
    MODEL_PATH = '/workspace/pipeline/weight/weight.pth'
    
    config = load_yml(CONFIG_PATH)
    model = TorchNN(input_size=config['data']['n_feature'],
                    hidden_size=512,
                    n_class=config['data']['n_class'])

    model.load_state_dict(torch.load(MODEL_PATH))

    train_df = load_pickle(DATA_PATH)['df']
    target = config['data']['target']

    x_train, y_train = train_df.drop(target, axis=1).values, train_df[target].values
    x_train_var = Variable(torch.FloatTensor(x_train), requires_grad=False) 

    with torch.no_grad():
        result = model(x_train_var)

    y_proba, y_pred = torch.max(result, 1)
    y_pred = y_pred.data.cpu().numpy()

    correct = np.sum(y_pred == y_train)
    print(f"{correct/len(y_pred)}")