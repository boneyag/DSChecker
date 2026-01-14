import torch
import torch.nn as nn
import torch.nn.functional as F


class MinimalCTC(nn.Module):
    def __init__(
        self, input_size, vocab_size, dropout_rate=0.0, ignore_id=-1, reduce=True
    ):
        super().__init__()
        self.ctc_lo = nn.Linear(input_size, vocab_size)
        self.dropout_rate = dropout_rate
        self.ignore_id = ignore_id
        self.reduce = reduce
        self.loss_fn = nn.CTCLoss(blank=0, reduction="sum" if reduce else "none")

    def forward(self, hs_pad, hlens, ys_pad):
        """CTC forward"""
        ys = [y[y != self.ignore_id] for y in ys_pad]
        hlens = torch.tensor(hlens, dtype=torch.int32)
        olens = torch.tensor([y.size(0) for y in ys], dtype=torch.int32)

        dtype = hs_pad.dtype

        if dtype == torch.float16:
            hs_pad = hs_pad.to(dtype=torch.float32)

        ys_hat = self.ctc_lo(F.dropout(hs_pad, p=self.dropout_rate))
        ys_true = torch.cat(ys).int()

        ys_hat = ys_hat.transpose(0, 1)

        ys_true = ys_true.to(ys_hat.device)
        loss = self.loss_fn(ys_hat, ys_true, hlens, olens).to(dtype=hs_pad.dtype)

        if self.reduce:
            loss = loss.sum()

        return loss


def minimal_example():
    batch_size = 2
    max_time_steps = 10
    input_dim = 10
    vocab_size = 5

    hs_pad = torch.randn(batch_size, max_time_steps, input_dim).half()
    hlens = [8, 6]
    ys_pad = []
    for _ in range(batch_size):
        label_length = torch.randint(3, 5, (1,)).item()
        ys_pad.append(torch.randint(1, vocab_size, (label_length,)))

    max_label_length = max(y.size(0) for y in ys_pad)
    padded_ys = torch.full((batch_size, max_label_length), -1, dtype=torch.long)
    for i, y in enumerate(ys_pad):
        padded_ys[i, : y.size(0)] = y

    ctc_module = MinimalCTC(input_dim, vocab_size)

    loss = ctc_module(hs_pad, hlens, padded_ys)
    print(loss)


if __name__ == "__main__":
    minimal_example()
