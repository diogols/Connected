import numpy as np

my_list = range(100)

prob = 1.5

mask = np.random.binomial(1, prob, len(my_list))

selected = [elem for keep, elem in zip(mask, my_list) if keep]

print(len(selected))
