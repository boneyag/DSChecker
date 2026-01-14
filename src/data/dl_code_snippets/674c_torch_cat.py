import torch
import torch.nn as nn

torch.manual_seed(0)


class DummyAttention(nn.Module):
    def forward(self, query, key, value, mask):
        return query


class DummyLinear(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)

    def forward(self, x):
        return self.linear(x)


class DecoderLayer(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.src_attn = DummyAttention()
        self.concate_linear2 = DummyLinear(2 * hidden_size, hidden_size)

    def forward(self, x, memory, memory_mask):
        x_concat = torch.cat((x, self.src_attn(x, memory, memory, memory_mask)), dim=-1)
        x = self.concate_linear2(x_concat)
        return x


batch_size = 2
seq_len_tgt = 10
hidden_size = 5

tgt = torch.randn(batch_size, seq_len_tgt, hidden_size)
memory = torch.randn(batch_size, 20, hidden_size)
memory_mask = None

decoder_layer = DecoderLayer(hidden_size)

output = decoder_layer(tgt, memory, memory_mask)
print("Output shape:", output.shape)
