import os
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class Base:
    def __init__(self, X, y, Xnames, ynames, return_test, scale_X, scale_y, 
                mean_normalize_y, noisy, test_train_ratio, s_to_n_ratio,
                noise_variance, scaler, random_state, backend=None):

        if backend is not None:        
            self.set_backend(backend)

        self.return_test = return_test
        self.X_test = None
        self.Xnames = Xnames
        self.ynames = ynames

        assert len(X.shape) == 2, "X should have shape (*,*) but has "+str(X.shape)
        assert len(y.shape) == 2, "y should have shape (*,1) but has "+str(y.shape)
        assert y.shape[1] == 1, "y should have shape (*,1) but has "+str(y.shape)
        assert X.shape[0] == y.shape[0], "X and y must be of the same length"
        self.X = X
        self.X_scaled = np.array(X)
        self.y = y
        self.y_scaled = np.array(y)
        self.N = X.shape[0]

        if noisy:
            np.random.seed(random_state)
            if s_to_n_ratio!=None and noise_variance!=None:
                raise ValueError("set either s_to_n_ratio OR noise_variance")    
            elif s_to_n_ratio != None:
                var_y = np.var(y)
                self.y_noisy = y + np.random.normal(0, var_y/s_to_n_ratio, (self.N, 1))
            elif noise_variance!=None:
                self.y_noisy = y + np.random.normal(0, noise_variance, (self.N, 1))
            else:
                raise ValueError("noisy=True but s_to_n_ratio or noise_variance not specified")
        else:
            self.y_noisy = y
        self.y_noisy_scaled = np.array(self.y_noisy)

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
            self._scale_y(scaler='std', with_std=False)
        else:
            raise ValueError("set either scale_y=True OR mean_normalize_y=True")

    def get_data(self):
        return self.transform(self.X_scaled, self.y_noisy_scaled, self.X_test_scaled)

    def transform(self, X, y, X_test):
        backend = self.get_backend()
        if backend == 'numpy':
            if self.return_test:
                return X, y, X_test
            return X, y
        elif backend == 'tf':
            import tensorflow as tf
            if self.return_test:
                return tf.convert_to_tensor(X), \
                tf.convert_to_tensor(y), \
                tf.convert_to_tensor(X_test)
            return tf.convert_to_tensor(X), tf.convert_to_tensor(y)
        elif backend == 'torch':
            import torch
            if self.return_test:
                return torch.tensor(X), \
                    torch.tensor(y), \
                    torch.tensor(X_test)
            return torch.tensor(X), torch.tensor(y)
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

        self.X_scaled = self.Xscaler.fit_transform(self.X)
        if self.return_test:
            self.X_test_scaled = self.Xscaler.transform(self.X_test)

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

        self.y_scaled = self.yscaler.fit_transform(self.y)
        self.y_noisy_scaled = self.yscaler.transform(self.y_noisy)
    
    def _plot(self, ax, **kwargs):
        ax.plot(self.X, self.y, label='True f')
        ax.scatter(self.X, self.y_noisy, label='data', **kwargs)
        ax.set_xlabel(self.Xnames[0])
        ax.set_ylabel(self.ynames[0])
        ax.legend()
        return ax

    def plot(self, ax=None, **kwargs):
        if ax is not None:
            return self._plot(ax, **kwargs)
        
        try:
            plt
        except NameError:
            import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        return self._plot(ax, **kwargs)