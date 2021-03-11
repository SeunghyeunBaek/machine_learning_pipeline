# from module.class_base import BaseModel
from model.architecture import TorchNN
from torch.autograd import Variable
import torch

from module.util import load_pickle, load_yml, set_logger
from tqdm import tqdm
import numpy as np
import random
import os

# from torchsummary import summary

"""
Kears, tensorflow, pytorch

"""

random_seed = 42
torch.manual_seed(random_seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
np.random.seed(random_seed)
random.seed(random_seed)

def train(x_train, y_train,
          batch_size, n_epoch,
          model, optimizer, criterion,
          logger,
          verbose=100,
          debug=False):

    n_batch = len(x_train) // batch_size  # Number of batches
    train_loss = 0
    train_loss_min = np.Inf

    for epoch_id in tqdm(range(n_epoch)):

        for batch_id in range(n_batch):
            
            # Set batch index
            start_data_id = batch_id * batch_size
            end_data_id = start_data_id + batch_size

            # Convert data to tensor
            x_var = Variable(torch.FloatTensor(x_train[start_data_id: end_data_id])).cuda()
            y_var = Variable(torch.tensor(y_train[start_data_id: end_data_id])).cuda()

            optimizer.zero_grad()
            output = model(x_var)  # Forward
            loss = criterion(output, y_var)
            loss.backward()  # Backward
            optimizer.step()
            
            #TODO: log template
            value, label = torch.max(output, 1)  # Get max proba
            n_tp = np.sum(label.data.cpu().numpy() == y_train[start_data_id:end_data_id]) # Check tp
            train_loss += loss.item() * batch_size
        
        # For each epoch
        train_loss = train_loss / len(x_train)

        if train_loss <= train_loss_min:
            msg = f"Validation loss decreased {train_loss_min} -> {train_loss}"
            train_loss_min = train_loss
            #weight_name = f'weight_{epoch_id}_{round(train_loss_min, 5)}.pth'
            weight_name = 'weight.pth'
            weight_path = os.path.join(WEIGHT_DIR, weight_name)
            if not debug:
                torch.save(model.state_dict(), weight_path)
                logger.info(msg)

        if epoch_id % verbose == 0:
            train_accuracy = round(n_tp / len(y_train[start_data_id: end_data_id]), 3)
            msg = f"\n Epoch: {epoch_id} train loss: {train_loss} train accuaracy: {train_accuracy}"
            if not debug:
                logger.info(msg)


if __name__ == '__main__':

    WEIGHT_DIR = '/workspace/pipeline/weight/'
    DATA_PATH = '/workspace/pipeline/output/data/train_processed_data.pkl'
    CONFIG_PATH = '/workspace/pipeline/config/train_config.yml'
    LOGGER_DIR = '/workspace/pipeline/log/'

    logger = set_logger(name='train', dir=LOGGER_DIR, show_logging=False)
    config = load_yml(CONFIG_PATH)
    train_df = load_pickle(DATA_PATH)['df']
    target = config['data']['target']

    x_train, y_train = train_df.drop(target, axis=1).values, train_df[target].values
    
    model = TorchNN(input_size=config['data']['n_feature'], 
                    hidden_size=512,
                    n_class=config['data']['n_class']).cuda()
    batch_size = 32

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=config['train']['learning_rate'])
    
    # Summary
    # summary(model, (batch_size, config['data']['n_feature']))
    
    # Train
    train(x_train=x_train, y_train=y_train,
          batch_size=config['train']['batch_size'],
          n_epoch=config['train']['n_epoch'],
          model=model, optimizer=optimizer, criterion=criterion,
          logger=logger,
          verbose=100)