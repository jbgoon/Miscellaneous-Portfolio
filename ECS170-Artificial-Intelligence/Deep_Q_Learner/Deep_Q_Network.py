from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.autograd as autograd
import math, random
USE_CUDA = torch.cuda.is_available()
Variable = lambda *args, **kwargs: autograd.Variable(*args, **kwargs).cuda() if USE_CUDA else autograd.Variable(*args, **kwargs)

class QLearner(nn.Module):
    def __init__(self, env, num_frames, batch_size, gamma, replay_buffer):
        super(QLearner, self).__init__()

        self.batch_size = batch_size
        self.gamma = gamma
        self.num_frames = num_frames
        self.replay_buffer = replay_buffer
        self.env = env
        self.input_shape = self.env.observation_space.shape
        self.num_actions = self.env.action_space.n

        self.features = nn.Sequential(
            nn.Conv2d(self.input_shape[0], 32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU()
        )
        
        self.fc = nn.Sequential(
            nn.Linear(self.feature_size(), 512), # creating a neural network layer with input of image size, output of 512 nodes
            nn.ReLU(), # Activation function. Not sure what this means. See: 
            nn.Linear(512, self.num_actions) # another layer that goes from 512 nodes to output number of nodes
        )
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x # The output of the neural network, should be all of the values for each action
    
    def feature_size(self):
            return self.features(autograd.Variable(torch.zeros(1, *self.input_shape))).view(1, -1).size(1)
    
    def act(self, state, epsilon):
        # EPSILON: At start, do random actions often so that we don't get stuck in a rut of overfitting. But
        # after some time, start to do the right move more and more often

        if random.random() > epsilon:
            state = Variable(torch.FloatTensor(np.float32(state)).unsqueeze(0), requires_grad=True)
            action_tensor = self.forward(state)

            #max function outputs tuple (value, index) of the max entry of the action tensor
            qvalue, action = torch.max(action_tensor, 1)

        else:
            action = random.randrange(self.env.action_space.n)
        return action

    def copy_from(self, target):
        self.load_state_dict(target.state_dict())

        
def compute_td_loss(model, target_model, batch_size, gamma, replay_buffer):

    # get tensors for batch data from replay buffer
    state, action, reward, next_state, done = replay_buffer.sample(batch_size)

    state = Variable(torch.FloatTensor(np.float32(state)).squeeze(1)) #added squeeze(1), probably not necessary
    next_state = Variable(torch.FloatTensor(np.float32(next_state)).squeeze(1), requires_grad=True)
    action = Variable(torch.LongTensor(action))
    reward = Variable(torch.FloatTensor(reward))
    done = Variable(torch.FloatTensor(done))

    # Calculate the expected q value using the target model
    t = target_model.forward(next_state) 
    expected_qvalue = torch.max(t, 1)[0] # use max because we are finding the q value of the best-action/nextstate pair
    expected_qvalue = reward + expected_qvalue*gamma*(1-done)
    expected_qvalue = expected_qvalue.unsqueeze(1)
    
    # Calculate the actual q value using the model
    o = model.forward(state) 
    qvalue = torch.gather(o, 1, action.unsqueeze(1)) # instead of gtting max-value action, get action that was given to us

    loss = (qvalue-expected_qvalue) ** 2
    return loss.sum() # Returns a tensor with the average loss value of all 32 samples


class ReplayBuffer(object):
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        state = np.expand_dims(state, 0)
        next_state = np.expand_dims(next_state, 0)

        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        # Randomly sampling data with specific batch size from the buffer
        # Only sample a batch-size amount of frames from the buffer

        #Basic idea: Generate random indices. Add buffer tuples, which correspond to indices, to a list (called batch)
        #Then, loop through the tuples in batch to get a list of each element. Return these lists
        batch = []
        indices = np.random.randint(1, len(self.buffer), batch_size)
        for item in indices:
            batch.append(self.buffer[item])
        batch1 = zip(*batch) #similar to matrix transposition. Takes all the first items of each list and puts those in a list, etc.
        state, action, reward, next_state, done = batch1
        return np.array(state), np.array(action, dtype=np.int64), np.array(reward, dtype=np.float32), np.array(next_state), np.array(done, dtype=np.bool)

    def __len__(self):
        return len(self.buffer)
