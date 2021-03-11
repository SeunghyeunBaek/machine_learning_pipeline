
import torch

class TorchNN(torch.nn.Module):
    """
    fc: fully connected layer
    """
    def __init__(self, input_size, hidden_size, n_class):
        super(TorchNN, self).__init__()
        self.fc1 = torch.nn.Linear(input_size, hidden_size)
        self.fc2 = torch.nn.Linear(hidden_size, hidden_size)
        self.fc3 = torch.nn.Linear(hidden_size, n_class)
        self.relu = torch.nn.ReLU()
        self.dropout = torch.nn.Dropout(0.2)


    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc3(x)
        return x