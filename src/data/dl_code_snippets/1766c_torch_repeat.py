import torch

torch.manual_seed(0)

n = 128
input = torch.randn(24, 2, 3, 384, 384)

if len(input.shape) < 1:
    raise AssertionError(input.shape)

identity = torch.eye(n, device=input.device, dtype=input.dtype)
identity = identity[None].expand(input.shape[0], n, n)
print(identity.shape)
