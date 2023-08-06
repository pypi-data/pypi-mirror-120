import tiggy.rl_utils as utils
import numpy as np
import torch.nn as nn
import torch
import torch.nn.functional as F

class Agent(nn.Module):
    def __init__(self, policy_net, policy_net_settings, value_net, value_net_settings):
        super().__init__()
        self.policy_net = policy_net(**policy_net_settings).cuda()
        self.value_net = value_net(**value_net_settings).cuda()
        self.policy_optimizer = torch.optim.AdamW(self.policy_net.parameters(), 3e-4)
        self.value_optimizer = torch.optim.AdamW(self.value_net.parameters(), 3e-4)

    def move(self, x, legal):
        p = self.use_policy(x, legal).cpu().numpy()
        moves = utils.get_moves(p).astype(np.int64)
        return moves

    def use_policy(self, x, legal):
        logits = self.policy_net(x.cuda())
        logits[~legal.cuda()] = float('-inf')
        p = F.softmax(logits, dim=-1)
        return p

    def evaluate(self, x):
        value = self.value_net(x.cuda())
        return value