import os
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class Base:
    def __init__(self, X, y, return_test, scale_X, scale_y, 
                mean_normalize_y, noisy, test_train_ratio, s_to_n_ratio,
                noise_variance, scaler='std', backend=None, link=None, name=None):

        if backend:        
            self.set_backend(backend)

        self.return_test = return_test
        self.X_test = None

        if X is None:
            pass
        assert len(X.shape) == 2, "X should have shape (*,*) but has "+str(X.shape)
        assert len(y.shape) == 2, "y should have shape (*,1) but has "+str(y.shape)
        assert y.shape[1] == 1, "y should have shape (*,1) but has "+str(y.shape)
        assert X.shape[0] == y.shape[0], "X and y must be of the same length"
        self.X = X
        self.N = X.shape[0]
        if noisy:
            if s_to_n_ratio!=None and noise_variance!=None:
                raise ValueError("set either s_to_n_ratio OR noise_variance")    
            if s_to_n_ratio != None:
                var_y = np.var(y)
            self.y = y + np.random.normal(0, var_y/s_to_n_ratio, (self.N, 1))
        else:
            self.y = y

        if return_test:
            Min = X.min()
            Max = X.max()
            Range = Max-Min
            if test_train_ratio != None:
                n = self.N*test_train_ratio
            else:
                n = self.N
            self.X_test = np.linspace(Min-Range/10, Max+Range/10, n).reshape(-1,1)
        
        if scale_X:
            self._scale_X(scaler)
        
        if scale_y and mean_normalize_y:
            raise ValueError("set either scale_y=True OR mean_normalize_y=True")
        elif scale_y:
            self._scale_y(scaler)
        elif mean_normalize_y:
            self._scale_y('std', with_std=False)
        else:
            raise ValueError("set either scale_y=True OR mean_normalize_y=True")

    def get_data(self):
        return self.transform(self.X, self.y, self.X_test)

    def transform(self, X, y, X_test):
        backend = self.get_backend()
        if backend == 'numpy':
            if self.return_test:
                return self.X, self.y, self.X_test
            return self.X, self.y
        elif backend == 'tf':
            import tensorflow as tf
            if self.return_test:
                return tf.convert_to_tensor(self.X), tf.convert_to_tensor(self.y), tf.convert_to_tensor(self.X_test)
            return tf.convert_to_tensor(self.X), tf.convert_to_tensor(self.y)
        elif backend == 'torch':
            import torch
            if self.return_test:
                return torch.tensor(self.X), torch.tensor(self.y), torch.tensor(self.X_test)
            return torch.tensor(self.X), torch.tensor(self.y)
        else:
            raise NotImplementedError("This error should be handled when called set_backend")
    
    def set_backend(self, backend):
        os.environ['BACKEND'] = backend

    def get_backend(self):
        return os.environ['BACKEND']
    
    def _scale_X(self, scaler='std', with_mean=True, with_std=True, feature_range=(0,1)):
        """
        Scaling X data
        """
        if scaler == 'minmax':
            self.Xscaler = MinMaxScaler(feature_range=feature_range)
        elif scaler == 'std':
            self.Xscaler = StandardScaler(with_mean=with_mean, with_std=with_std)
        else:
            raise NotImplementedError('scaler: '+scaler)

        self.X = self.Xscaler.fit_transform(self.X)
        if self.return_test:
            self.X_test = self.Xscaler.transform(self.X_test)

    def _scale_y(self, scaler='std', with_mean=True, with_std=True, feature_range=(0,1)):
        """
        Scaling y data
        """
        if scaler == 'minmax':
            self.yscaler = MinMaxScaler(feature_range=feature_range)
        elif scaler == 'std':
            self.yscaler = StandardScaler(with_mean=with_mean, with_std=with_std)
        else:
            raise NotImplementedError('scaler: '+scaler)

        self.y = self.yscaler.fit_transform(self.y)