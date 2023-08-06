import torch
import tiggy.rl_utils as utils
import itertools
import numpy as np
import torch.nn.functional as F


class Trainer:
    def __init__(self, env, agent, parallel_size, experience_threshold, batch_size=256, decay_factor=.97):
        self.env = env
        self.agent = agent
        self.parallel_size = parallel_size
        self.envs = [self.env() for _ in range(parallel_size)]
        self.repr_storage = [[] for env in self.envs]
        self.move_storage = [env.reset() for env in self.envs]
        self.big_storage = []
        self.experience_threshold = experience_threshold
        self.batch_size = batch_size
        self.decay_factor = decay_factor


    def step(self):
        inputs = utils.unpack(self.move_storage)
        with torch.no_grad():
            moves = self.agent.move(torch.from_numpy(inputs['obs']).float(), torch.from_numpy(inputs['legal']))
            values = self.agent.evaluate(torch.from_numpy(inputs['obs']).float()).cpu().numpy()

        self.move_storage = [env.move(move) for env, move in zip(self.envs, moves)]
        unpacked_env_outputs = utils.unpack(self.move_storage)
        for i, (obs, legal, reward, is_final, move, value) in enumerate(zip(inputs['obs'], inputs['legal'], unpacked_env_outputs['reward'], unpacked_env_outputs['is_final'], moves, values)):
            self.repr_storage[i] += [{'obs':obs, 'legal':legal, 'reward':reward, 'is_final':is_final, 'move':move, 'value':value}]
            if is_final:
                self.big_storage += [self.repr_storage[i]]
                self.repr_storage[i] = []
                if len(self.big_storage) >= self.experience_threshold:
                    self.train()

    def train(self):
        big_storage = utils.decay_rewards(self.big_storage, self.decay_factor)
        big_storage = [record for storage in big_storage for record in storage]
        unpacked_big_storage = utils.unpack(big_storage)

        x = torch.from_numpy(unpacked_big_storage['obs']).float().cuda()
        rewards = torch.from_numpy(np.array(unpacked_big_storage['reward'])).cuda()
        moves = torch.from_numpy(np.array(unpacked_big_storage['move'])).long().cuda()
        legal = torch.from_numpy(unpacked_big_storage['legal']).cuda()

        with torch.no_grad():
            advantages = rewards - torch.reshape(self.agent.evaluate(x), (-1,))
            std, mean = torch.std_mean(advantages)
            advantages = (advantages-mean)/std

        # with torch.enable_grad():
        p = self.agent.use_policy(x, legal)
        loss = torch.mean(F.cross_entropy(p, moves, reduction='none') * advantages)
        self.agent.policy_optimizer.zero_grad()
        loss.backward()
        self.agent.policy_optimizer.step()

        v = self.agent.evaluate(x)
        loss = F.mse_loss(v, torch.reshape(rewards, (-1, 1)).float())
        self.agent.value_optimizer.zero_grad()
        loss.backward()
        self.agent.value_optimizer.step()

        self.big_storage = []
