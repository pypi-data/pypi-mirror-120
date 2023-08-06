import numpy as np
from .base import Base

class Smooth1D(Base):
    def __init__(self, return_test=True, scale_X = True, scale_y = False, 
                mean_normalize_y=True, noisy=True, test_train_ratio=2, 
                s_to_n_ratio=3, noise_variance=None, scaler='std', 
                min=-2, max=2, samples=101, random_state=0, backend=None):

        np.random.seed(random_state)
        X = np.linspace(min, max, samples).reshape(-1,1)
        y = np.sin(X) + 2 * np.exp(-30 * np.square(X))
        
        super().__init__(X, y, return_test, scale_X, scale_y, 
                mean_normalize_y, noisy, test_train_ratio, s_to_n_ratio,
                noise_variance, scaler, backend=backend)