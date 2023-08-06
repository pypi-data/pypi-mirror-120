from .backend_common import backend_test
import regdata as rd

def test_step():
    backend_test(rd.Step)