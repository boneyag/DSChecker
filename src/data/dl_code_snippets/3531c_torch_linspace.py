import torch

torch.manual_seed(0)


def create_timestep(num_steps, device="cpu"):
    return torch.linspace(0, 1, num_steps, device=device)


device = "cuda" if torch.cuda.is_available() else "cpu"
x = torch.randn(10, device=device)

time_steps = create_timestep(10, device=device)
res = x + time_steps
print(res)
