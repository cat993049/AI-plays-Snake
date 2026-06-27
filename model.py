import torch
import torch.nn as nn
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size).to(device)
        self.fc2 = nn.Linear(hidden_size, output_size).to(device)

    def forward(self,x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def save(self,name="model.pth"):
        torch.save(self.state_dict(), os.path.join(".",name))