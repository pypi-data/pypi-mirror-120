# RegData

[![CI](https://github.com/patel-zeel/regdata/workflows/CI/badge.svg)](https://github.com/patel-zeel/regdata/actions?query=workflow%3ACI)

Collection of regression datasets.

* Get data in any framework: ```torch```, ```tensorflow``` or ```numpy```

## Install
```bash
pip install regdata
```
## Quick example

```python
import regdata as rd
rd.set_backend('torch') # numpy, tf (numpy is default)
X, y, X_test = rd.Step().get_data()
```

## Plot datasets to have a quick glance

```python
import regdata as rd
rd.Olympic().plot()
```

Checkout all plots [here](https://nbviewer.jupyter.org/github/patel-zeel/regdata/blob/main/notebooks/visualize.ipynb).

## Datasets

```python
from regdata import (
    Step,
    Olympic,
    Smooth1D
)
```

## References

* [Step](http://inverseprobability.com/talks/notes/deep-gaussian-processes.html)
* [Olympic](http://inverseprobability.com/talks/notes/deep-gaussian-processes.html)
* [Smooth1D](http://www.stat.cmu.edu/~kass/papers/bars.pdf) - Example 2