from .lib import *

def backend_test(func, **kwargs):
    X, y, X_test = func(backend='numpy', **kwargs).get_data()
    assert X.dtype == y.dtype == X_test.dtype == np.float64
    X, y, X_test = func(backend='torch', **kwargs).get_data()
    assert X.dtype == y.dtype == X_test.dtype == torch.float64
    X, y, X_test = func(backend='tf', **kwargs).get_data()
    assert X.dtype == y.dtype == X_test.dtype == tf.float64

def plotting_test(func, **kwargs):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    func(backend='numpy', **kwargs).plot(ax=ax)
    fig.savefig('figures/'+func.__name__+'.pdf')