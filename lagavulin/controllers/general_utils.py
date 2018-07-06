import hyperdash
from contextlib import contextmanager


class debugHyperDash(object):
    def metric(self, name, value):
        print(f"| {name}: {value:10f} |")

    def param(self, name, value):
        pass

    def end(self):
        pass


@contextmanager
def hyper_dash_manager(exp_name, debug=False):
    """
    debug=True の時に、hyperdashにログを送信しないダミーインスタンスを返す。
    """
    if debug:
        exp = debugHyperDash()
    else:
        exp = hyperdash.Experiment(exp_name)

    try:
        yield exp
    finally:
        exp.end()
