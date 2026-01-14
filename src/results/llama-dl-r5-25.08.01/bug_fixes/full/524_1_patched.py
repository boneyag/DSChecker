import torch

torch.manual_seed(0)


def apply_mask(img):
    b, c, h, w = img.shape
    mask = torch.randn(b, 1, h, w).to(device=img.device)
    mask = mask.expand(b, c, h, w)
    masked_img = img * mask
    return masked_img


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
img = torch.randn(2, 3, 128, 128).to(device=device)

masked_imaged = apply_mask(img)
