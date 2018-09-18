import pandas as pd
import numpy as np

data = pd.read_excel(r'9架无人机航线.xlsx')
print(data)
print(data.shape)
print(np.array(data))
print(np.array(data)[:, 1:].shape)
print(np.reshape(np.array(data)[:, 1:], [60, 9]))
