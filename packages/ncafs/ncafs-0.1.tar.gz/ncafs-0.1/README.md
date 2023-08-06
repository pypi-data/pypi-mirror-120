# NCAFS

Neighborhood Component Analysis Feature Selection

## Getting started

### Classification
```python
from ncafs import NCAFSC
from sklearn import datasets

X, y = datasets.make_classification(
    n_samples=1000,
    n_classes=5,
    n_features=20,
    n_informative=100,
    n_redundant=0,
    n_repeated=0,
    flip_y=0.1,
    class_sep=0.5,
    shuffle=False,
    random_state=0
)

fs_clf = NCAFSC()
fs_clf.fit(X, y)
w = fs_clf.weights_
```

### Regression
```python
from ncafs import NCAFSR
from sklearn import datasets

X, y, coef = datasets.make_regression(
    n_samples=1000,
    n_features=100,
    n_informative=20,
    bias=0,
    noise=1e-3,
    coef=True,
    shuffle=False,
    random_state=0
)

fs_reg = NCAFSR()
fs_reg.fit(X, y)
w = fs_reg.weights_
```

## References

1. Yang, W., Wang, K., & Zuo, W. (2012). Neighborhood component feature selection for high-dimensional data. J. Comput., 7(1), 161-168.
2. Amankwaa-Kyeremeh, B., Greet, C., Zanin, M., Skinner, W., & Asamoah, R. K. Selecting Key Predictor Parameters for Regression Analysis using Modified Neighbourhood Component Analysis (NCA) Algorithm.
