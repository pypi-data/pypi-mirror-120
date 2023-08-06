from .lib import *

def backend_test(func, **kwargs):
    X, y, X_test = func(backend='numpy', **kwargs).get_data()
    assert X.dtype == y.dtype == X_test.dtype == np.float64
    X, y, X_test = func(backend='torch', **kwargs).get_data()
    assert X.dtype == y.dtype == X_test.dtype == torch.float64
    X, y, X_test = func(backend='tf', **kwargs).get_data()
    assert X.dtype == y.dtype == X_test.dtype == tf.float64