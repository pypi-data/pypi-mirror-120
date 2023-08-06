from .transformer_layers import *
import torch.nn as nn
import torch
import einops


class ShuffleFormer(nn.Module):
    def __init__(self, n_vocab, depth, hidden_dim, seq_len, shuffle_dim, heads, n_buckets):
        super().__init__()
        self.pos_embedding = nn.Parameter(torch.zeros((seq_len, hidden_dim)))
        self.embedding = nn.Embedding(n_vocab, hidden_dim)
        self.layers = nn.ModuleList([])
        for _ in range(depth):
            self.layers += [PreNorm(hidden_dim), ShuffleFormerLayer(seq_len, hidden_dim, shuffle_dim, heads, n_buckets),
                            PreNorm(hidden_dim), FeedforwardLayer(hidden_dim)]

    def forward(self, x, gamma):
        b, *_ = x.shape
        x = self.embedding(x)
        x += einops.repeat(self.pos_embedding, 'n d -> b n d', b=b)
        for layer in self.layers:
            x = layer(x, gamma)

        return x


class Transformer(nn.Module):
    def __init__(self, depth, hidden_dim, seq_len, heads, n_vocab=None, input_dim=None, use_cls_token=False, out_dim=None):
        super().__init__()
        self.pos_embedding = nn.Parameter(torch.zeros((seq_len, hidden_dim)))
        if n_vocab is not None:
            self.embedding = nn.Embedding(n_vocab, hidden_dim)
        elif input_dim is not None:
            self.embedding = nn.Linear(input_dim, hidden_dim)
        self.use_cls_token = use_cls_token
        if use_cls_token:
            self.cls_token = nn.Parameter(torch.zeros((hidden_dim)))

        self.out_projection = nn.Linear(hidden_dim, out_dim) if out_dim is not None else nn.Identity()

        self.layers = nn.ModuleList([])
        for _ in range(depth):
            self.layers += [PreNorm(hidden_dim), Attention(hidden_dim, heads),
                            PreNorm(hidden_dim), FeedforwardLayer(hidden_dim)]

    def forward(self, x):
        b, *_ = x.shape
        x = self.embedding(x)
        x += einops.repeat(self.pos_embedding, 'n d -> b n d', b=b)
        if self.use_cls_token:
            x = torch.cat([x, einops.repeat(self.cls_token, 'b -> b n d', b=b, n=1)], dim=1)
        for layer in self.layers:
            x = layer(x)

        if self.use_cls_token:
            return self.out_projection(x[:, -1])
        return self.out_projection(x[:, -1])