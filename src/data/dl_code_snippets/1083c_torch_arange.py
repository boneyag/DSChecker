import torch

torch.manual_seed(0)


def max_prediction_mask(gold_labels, device="cpu"):
    return torch.arange(gold_labels.numel(), device=device)


dev = "cuda" if torch.cuda.is_available() else "cpu"
gold_labels = torch.tensor([1, 0, 2, 1]).to(dev)

res = torch.where(max_prediction_mask(gold_labels, device=dev) == gold_labels)[0]
print(res)
