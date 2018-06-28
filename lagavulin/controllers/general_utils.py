
import hyperdash
from contextlib import contextmanager

@contextmanager
def hyper_dash_manager(exp_name):
    exp = hyperdash.Experiment(exp_name)
    try:
        yield exp
    finally:
        exp.end()

