from .common import backend_test
import regdata as rd

def test_step():
    backend_test(rd.Step)

def test_smooth1d():
    backend_test(rd.Smooth1D)