import os

def set_backend(backend):
    if backend == 'numpy':
        try:
            import numpy
        except:
            raise ImportError("Numpy is not installed")
    elif backend == 'torch':
        try:
            import torch
        except:
            raise ImportError("Torch is not installed")
    elif backend == 'tf':
        try:
            import tensorflow
        except:
            raise ImportError("Tensorflow is not installed")
    else:
        raise NotImplementedError('backend "'+ backend +'" is not implemented')

    os.environ['BACKEND'] = backend