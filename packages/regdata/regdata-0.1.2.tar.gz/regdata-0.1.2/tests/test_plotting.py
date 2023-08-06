from .common import plotting_test
import regdata as rd

def test_step():
    plotting_test(rd.Step)

def test_smooth1d():
    plotting_test(rd.Smooth1D)