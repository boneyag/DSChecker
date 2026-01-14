import torch
import torch.nn as nn


class SimpleAttention(nn.Module):
    def __init__(self, embed_dim):
        super().__init__()
        self.query = nn.Linear(embed_dim, embed_dim)
        self.key = nn.Linear(embed_dim, embed_dim)

    def forward(self, x, attn_mask=None):
        """
        x: (seq_len, batch, embed_dim)
        attn_mask: (seq_len, seq_len)
        """
        q = self.query(x)
        k = self.key(x)

        scores = torch.einsum("tbe,sbe->bts", q, k)

        if attn_mask is not None:
            scores = scores.masked_fill(attn_mask, -1e8)

        attention_weights = torch.softmax(scores, dim=-1)
        return attention_weights


seq_len = 128
batch_size = 2
embed_dim = 64

model = SimpleAttention(embed_dim).half()
input_tensor = torch.randn(seq_len, batch_size, embed_dim).half()

attn_mask = torch.randint(0, 2, (seq_len, seq_len)).bool()

output = model(input_tensor, attn_mask)
