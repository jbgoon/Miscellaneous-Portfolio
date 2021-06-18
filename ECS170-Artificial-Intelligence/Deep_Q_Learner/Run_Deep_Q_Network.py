from Wrapper.layers import *
from Wrapper.wrappers import make_atari, wrap_deepmind, wrap_pytorch
import math, random
import gym
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import torch.autograd as autograd 
import torch.nn.functional as F
USE_CUDA = torch.cuda.is_available()
from dqn import QLearner, compute_td_loss, ReplayBuffer

env_id = "PongNoFrameskip-v4"
env = make_atari(env_id)
env = wrap_deepmind(env)
env = wrap_pytorch(env)

num_frames = 1000000
batch_size = 32
gamma = 0.99
record_idx = 10000

replay_initial = 10000
replay_buffer = ReplayBuffer(100000)
model = QLearner(env, num_frames, batch_size, gamma, replay_buffer)
model.load_state_dict(torch.load("model_pretrained.pth", map_location='cpu'))

target_model = QLearner(env, num_frames, batch_size, gamma, replay_buffer)
target_model.copy_from(model)

optimizer = optim.Adam(model.parameters(), lr=0.00001)
if USE_CUDA:
    model = model.cuda()
    target_model = target_model.cuda()
    print("Using cuda")

epsilon_start = 1.0
epsilon_final = 0.01
epsilon_decay = 30000
epsilon_by_frame = lambda frame_idx: epsilon_final + (epsilon_start - epsilon_final) * math.exp(-1. * frame_idx / epsilon_decay)
# .01 + 0.99* 1/ e^(frame index / 30000)
# So epsilon starts at pretty much 1
# as frame index increases, exp will get larger so 1/exp will decrease, so the 0.99 term will decrease, leaving us with just the final
# half of num_frames will give us a value very close to final value. So it decays quickly.

losses = []
all_rewards = []
episode_reward = 0

state = env.reset()

for frame_idx in range(1, num_frames + 1): # QUESTION: Why is num_frames > replay_buffer capacity? replay_buffer should 
# overfill because num_frames is larger, so it will keep adding. Does it automatically expand when you push? I think it does expand,
# using the numpy expand_dims funciton

    #print("Frame: " + str(frame_idx))

    epsilon = epsilon_by_frame(frame_idx) # get the epsilon value
    action = model.act(state, epsilon) # This is where act function is used
    
    next_state, reward, done, _ = env.step(action) # look at next state to see if it gives us a reward
    replay_buffer.push(state, action, reward, next_state, done)
    
    state = next_state
    episode_reward += reward
    
    # if the game is over
    if done:
        state = env.reset()
        all_rewards.append((frame_idx, episode_reward)) # record reward for that game
        episode_reward = 0 # reset

    # Once the replay buffer has filled up enough
    if len(replay_buffer) > replay_initial:
        loss = compute_td_loss(model, target_model, batch_size, gamma, replay_buffer) # calculate the loss for the state
        optimizer.zero_grad() # reset gradient values
        loss.backward() # backpropogate loss
        optimizer.step() # Updates weight values
        losses.append((frame_idx, loss.data.cpu().numpy())) # hold loss in array

    if frame_idx % 10000 == 0 and len(replay_buffer) <= replay_initial:
        print('#Frame: %d, preparing replay buffer' % frame_idx)
        torch.save(model.state_dict(), "run11_start.pth")

    if frame_idx % 10000 == 0 and len(replay_buffer) > replay_initial:
        print('#Frame: %d, Loss: %f' % (frame_idx, np.mean(losses, 0)[1]))
        print('Last-10 average reward: %f' % np.mean(all_rewards[-10:], 0)[1])
        filename = "run11_model"+str(frame_idx)+".pth"
        torch.save(model.state_dict(), filename)
        lossScript=open("run11_losses.txt", "w")
        rewardScript=open("run11_rewards.txt", "w")
        lossScript.write(str(losses))
        rewardScript.write(str(all_rewards))
        lossScript.close()
        rewardScript.close()

    if frame_idx % 50000 == 0:
        target_model.copy_from(model) # How can we use the target model as the ideal mode, when every 50,000 frames we are setting it to our dumb model?
        # the target_model starts dumb but since its outputs are multiplied by gamma, added to reward, it will still lead the model to improve. Then use the new model
        # to make target_model that much better.



