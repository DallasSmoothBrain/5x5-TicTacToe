import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical

# what needs to happen?
# make the game logic able to interact with the agent
# convert the game board into a state that accounts for symetry
# create two neural networks that will play the game against one another (one plays as x, the other as o)
    # we will use the actor critic architecture
    # a neural net is probably overkill for this, but it's also cool
# save the weights of both networks
# get it to play against a player
