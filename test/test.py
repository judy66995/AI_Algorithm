import torch

x = torch.tensor([[1, 2], [3, 4]]) # 创建一个2x2的张量

# x = torch.tensor([[1, 2], [3, 4]], device='cuda') # 创建一个2x2的张量，并将其放置在GPU上
# print(x.device) # 输出张量所在的设备
print(torch.cuda.is_available()) # 检查CUDA是否可用

