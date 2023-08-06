# A simple pytorch based MNL lib
> Fit your Multinomial Logistic Regression with Pytorch


## Install

`pip install pytorch_mnl`

## How to use

import the lib

```python
import pandas as pd
from pytorch_mnl.core import *
```

load data

```python
data = pd.read_csv("./data/Iris.csv").drop("Id", axis=1)
```

choose x, y cols:

```python
x_cols=['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']
target_col = 'Species'
```

the number of classes to predict:

```python
n_targets = len(data[target_col].unique())
n_targets
```




    3



```python
X, y = prepare_data(data, x_cols=x_cols, target_col=target_col)
```

we get pytorch tensors ready to use!

```python
type(X), type(y)
```




    (torch.Tensor, torch.Tensor)



let's split in train/valid choosing a percenage as holdout, and choose a batch size to fit our model

```python
dls = DataLoaders.from_Xy(X, y, pct=0.2, batch_size=8)
```

as our model has 4 variables, we will fit a 4 MNL, with 3 targets.

```python
model = LinearMNL(len(x_cols), n_targets)
```

```python
learn = Learner(dls, model)
```

```python
learn.fit(25)
```





    epoch =   0, val_loss = 2.072, accuracy = 0.53
    epoch =   1, val_loss = 1.908, accuracy = 0.53
    epoch =   2, val_loss = 1.770, accuracy = 0.80
    epoch =   3, val_loss = 1.657, accuracy = 0.80
    epoch =   4, val_loss = 1.564, accuracy = 0.80
    epoch =   5, val_loss = 1.487, accuracy = 0.80
    epoch =   6, val_loss = 1.422, accuracy = 0.80
    epoch =   7, val_loss = 1.368, accuracy = 0.80
    epoch =   8, val_loss = 1.321, accuracy = 0.80
    epoch =   9, val_loss = 1.282, accuracy = 0.83
    epoch =  10, val_loss = 1.247, accuracy = 0.83
    epoch =  11, val_loss = 1.217, accuracy = 0.83
    epoch =  12, val_loss = 1.190, accuracy = 0.83
    epoch =  13, val_loss = 1.166, accuracy = 0.83
    epoch =  14, val_loss = 1.144, accuracy = 0.87
    epoch =  15, val_loss = 1.125, accuracy = 0.87
    epoch =  16, val_loss = 1.107, accuracy = 0.90
    epoch =  17, val_loss = 1.091, accuracy = 0.90
    epoch =  18, val_loss = 1.076, accuracy = 0.90
    epoch =  19, val_loss = 1.063, accuracy = 0.90
    epoch =  20, val_loss = 1.050, accuracy = 0.90
    epoch =  21, val_loss = 1.038, accuracy = 0.90
    epoch =  22, val_loss = 1.027, accuracy = 0.90
    epoch =  23, val_loss = 1.016, accuracy = 0.90
    epoch =  24, val_loss = 1.007, accuracy = 0.90

