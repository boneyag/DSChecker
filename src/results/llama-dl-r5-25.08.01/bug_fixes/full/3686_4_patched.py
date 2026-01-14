import torch


def calculate_mean(tensor_list):
    return torch.mean(torch.stack(tensor_list), dim=0)


num_tensors = 1000
tensor_size = (100, 100)
torch.manual_seed(0)
tensor_list = [torch.randn(tensor_size) for _ in range(num_tensors)]

mean = calculate_mean(tensor_list)
