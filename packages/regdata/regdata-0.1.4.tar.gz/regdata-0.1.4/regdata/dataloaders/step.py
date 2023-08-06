import numpy as np
from .base import Base

class Step(Base):
    def __init__(self, return_test=True, scale_X = True, scale_y = False, 
                mean_normalize_y=True, noisy=True, test_train_ratio=2, s_to_n_ratio=20,
                noise_variance=None, scaler='std', Min=-1, Max=1, num_low=25, num_high=25, 
                gap=-0.1, random_state=0, backend=None):
        
        synthetic = True
        np.random.seed(random_state)
        X = np.vstack((np.linspace(Min, -gap/2.0, num_low)[:, np.newaxis],
              np.linspace(gap/2.0, Max, num_high)[:, np.newaxis]))
        y = np.vstack((np.zeros((num_low, 1)), np.ones((num_high,1))))
        Xnames = ['X']
        ynames = ['y']
        super().__init__(X, y, Xnames, ynames, return_test, scale_X, scale_y, 
                mean_normalize_y, noisy, test_train_ratio, s_to_n_ratio,
                noise_variance, scaler, backend=backend, random_state=random_state, 
                synthetic=synthetic)