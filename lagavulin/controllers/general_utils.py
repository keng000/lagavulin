import hyperdash
from contextlib import contextmanager
class debugHyperDash(object):
    def metric(self, name, value):
        print(f"| {name}: {value:10f} |")

    def end(self):
        pass

@contextmanager
def hyper_dash_manager(exp_name, debug=False):

    if debug:
        exp = debugHyperDash()
    else:
        exp = hyperdash.Experiment(exp_name)

    try:
        yield exp
    finally:
        exp.end()

