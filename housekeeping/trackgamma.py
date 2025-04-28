import math

for epoch in range(100):
    gamma = math.exp(-epoch/100)

    print(epoch, gamma)