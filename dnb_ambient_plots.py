import numpy as np
import pandas as pd
from sklearn.preprocessing import PowerTransformer
import matplotlib.pyplot as plt

from classification import Classification

with open("data_collection/binary_dnb_ambient_train.csv", 'r') as f:
    csv_data = pd.read_csv(f)
if "MusicalKey" in csv_data.columns[5]:
    csv_data = csv_data.drop(columns="MusicalKey")  # this is bad data - codeified version of a musical key - meaningless and can't normalise
if "_id" in csv_data.columns[0]:
    csv_data = csv_data.drop(columns="_id")

data = np.array(csv_data.iloc[0:, 0:(len(csv_data.columns)-1)])
standardizer = PowerTransformer()  # defaults to zero-mean, unit-variance
# for col in data.T:
#     col_standardized = standardizer.fit_transform(col)
#     print(f'mean and variance of data: {np.mean(col_standardized), np.var(col_standardized)}')

data = standardizer.fit_transform(data)
print('mean and variance per column:')
for col in data.T:
    print(f'{np.mean(col), np.var(col)}')

select_data = data[:, 1: 3]
select_columns = csv_data.columns[1: 3]
X = pd.DataFrame(data=select_data, columns=select_columns)
# Then add a column of ones at the start for the intercept term
X.insert(0, "intercept", np.ones(len(X)))
print(X)

# Results need to be codified (not strings)
result = np.array(csv_data.iloc[0:, len(csv_data.columns)-1])
y = pd.Series(result)

# theta needs to be the same length as the number of features (including the extra column due to the intercept)
theta = np.ones(len(X.columns))
theta = pd.Series(theta)

vals = X.T.values[1:, :]
print(vals)

# Probably mixed up the labels of dnb/ambient and danceability and energy
dnb = (vals[0][:83], vals[1][:83])
ambient = (vals[0][87:], vals[1][87:])

data = (dnb, ambient)
colors = ("red", "green")
groups = ("dnb", "ambient")

# Create plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

for data, color, group in zip(data, colors, groups):
    x, y = data
    ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=30, label=group)

plt.title('Diff between dance and energy')
plt.ylabel('Danceability')
plt.xlabel('Energy')
plt.grid = True
plt.legend(loc=2)
plt.show()

