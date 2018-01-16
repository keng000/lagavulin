# coding: utf-8
import cProfile
import numpy as np
from scipy.stats import norm
import time
from tqdm import tqdm


class profilingAssistant(object):

    def profiling(self, func, *args, **kw):
        self.assert_func(func, *args, **kw)
        p = cProfile.Profile()
        p.enable()
        func(*args, **kw)
        p.disable()
        p.print_stats()

    def timeCalc(self, func, iteration=30, significance_level=0.05, *args, **kw):
        self.assert_func(func, *args, **kw)
        iterNum = iteration
        time_result = np.zeros(iterNum)

        for idx in tqdm(range(iterNum)):
            st = time.time()
            func(*args, **kw)
            time_result[idx] = (time.time() - st)

        mean = np.mean(time_result)
        sd = np.sqrt(np.var(time_result, ddof=0))
        coeff_range = norm.pdf(1 - significance_level / 2) * sd

        print("Mean:\t{:.4}".format(mean))
        print("SD:\t\t{:.4}".format(sd))
        print("Coef Interval:\t[{:.4} ~ {:.4}]".format(mean - coeff_range, mean + coeff_range))
        return mean

    def assert_func(self, func, *args, **kw):
        ans = func(*args, **kw)
        is_correct = self.is_correct(ans)
        print("Correct:", is_correct)
        assert is_correct is True, NotImplementedError("The implementation is incorrect.")

    def is_correct(self, output):
        """
        Compare the output with the prepared assumed output.
        :param output: the output from the function.
        :return: True or False. is the output is correct or not.
        """
        raise NotImplementedError("You should implement is_correct() before running.")
