import torch

torch.manual_seed(0)

n = 128
input = torch.randn(24, 2, 3, 384, 384)
print(type(input))
print(input.shape)
print(input.dtype)
print(input[:1, :1, :1, :3, :3])
if len(input.shape) < 1:
    raise AssertionError(input.shape)

identity = torch.eye(n, device=input.device, dtype=input.dtype)
identity = identity[None].repeat(input.shape[0], 1, 1)
print(identity.shape)
