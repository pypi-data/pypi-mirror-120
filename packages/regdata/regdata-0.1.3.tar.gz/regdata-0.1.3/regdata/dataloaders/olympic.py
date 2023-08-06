import os
import pandas as pd
import warnings
from .base import Base

class Olympic(Base):
    def __init__(self, return_test=True, scale_X = True, scale_y = False, 
                mean_normalize_y=True, noisy=True, test_train_ratio=2, s_to_n_ratio=20,
                noise_variance=None, scaler='std', random_state=0, backend=None):

        if not os.path.exists(os.environ['DATAPATH']+'olympic.csv'):
            warnings.warn('Olympic data not found. Downloading...')
            path = 'https://raw.githubusercontent.com/patel-zeel/regdata/main/archive/olympic_men100m.csv'
            os.system('wget '+path+' -O '+os.environ['DATAPATH']+'olympic.csv')
        data = pd.read_csv(os.environ['DATAPATH']+'olympic.csv')
        X = data['Year'].values.reshape(-1,1)
        y = data['Pace min/km'].values.reshape(-1,1)

        Xnames = ['Year']
        ynames = ['Pace min/km']
        super().__init__(X, y, Xnames, ynames, return_test, scale_X, scale_y, 
                mean_normalize_y, noisy, test_train_ratio, s_to_n_ratio,
                noise_variance, scaler, random_state, backend=backend)