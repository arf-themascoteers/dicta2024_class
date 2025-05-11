import torch

def inverse_sigmoid_torch(x):
    return -torch.log(1.0 / x - 1.0)



x = 4000
z = x/4200
p = torch.tensor([z])

y = inverse_sigmoid_torch(p)

print(y)