# coding: utf-8
import cProfile
import numpy as np
import pstats
from scipy.stats import norm
import time
from tqdm import tqdm

sort_by_cand = [
    'calls',  # 呼び出し数
    'cumulative',  # 累積時間
    'cumtime',  # 累積時間
    'file',  # ファイル名
    'filename',  # ファイル名
    'module',  # ファイル名
    'ncalls',  # 呼び出し数
    'pcalls',  # プリミティブな呼び出し回数
    'line',  # 行番号
    'name',  # 関数名
    'nfl',  # 関数名/ファイル名/行番号
    'stdname',  # 標準名
    'time',  # 内部時間
    'tottime' # 内部時間
]


class profilingAssistant(object):

    def profiling(self, func, sortby=None, **kw):
        p = cProfile.Profile()
        p.enable()
        func(**kw)
        p.disable()
        if sortby is None:
            p.print_stats()
        elif sortby in sort_by_cand:
            pstats.Stats(p).sort_stats(sortby).print_stats()
        else:
            raise ValueError("Unknown key for sort stats -> sortby:{}\nChoose from here.\n{}".format(sortby, sort_by_cand))

    def timeCalc(self, func, basefunc=None, iteration=30, significance_level=0.05, **kw):

        new_func_time_result = np.zeros(iteration)
        base_func_time_result = np.zeros(iteration)

        for idx in tqdm(range(iteration)):
            st = time.time()
            new_func_ret = func(**kw)
            new_func_time_result[idx] = (time.time() - st)

            if basefunc is not None:
                st = time.time()
                base_func_ret = basefunc(**kw)
                base_func_time_result[idx] = (time.time() - st)

                assert self.is_same(new_func_ret, base_func_ret), AssertionError(
                    "Implementation of the new function is incorrect.")

        new_mean = np.mean(new_func_time_result)
        new_sd = np.sqrt(np.var(new_func_time_result, ddof=0))
        base_mean = np.mean(base_func_time_result)
        base_sd = np.sqrt(np.var(base_func_time_result, ddof=0))

        if basefunc is None:
            coeff_range = norm.pdf(1 - significance_level / 2) * new_sd
            print("New Func Mean:\t{:.4}s".format(new_mean))
            print("New Func SD:\t\t{:.4}s".format(new_sd))
            print("Coef Interval:\t[{:.4}s ~ {:.4}s]".format(new_mean - coeff_range, new_mean + coeff_range))

        else:
            print("Base func Mean:\t{:.4}s".format(base_mean))
            print("New  func Mean:\t{:.4}s".format(new_mean))
            print("Efficiency:\t\tx {:.3}".format(base_mean / new_mean))

            diff_mean = new_mean - base_mean
            diff_sd = np.sqrt(np.var(new_func_time_result - base_func_time_result, ddof=0))
            coeff_range = norm.pdf(1 - significance_level / 2) * diff_sd
            print("Diff Coef Interval:\t[{:.4}s ~ {:.4}s]".format(diff_mean - coeff_range, diff_mean + coeff_range))

    def is_same(self, left, right):
        """
        This function will compare the two output which are from the base function and the new function.
        :param left, right: This is the output from the two function.
        :return: if the output is same then True, else False
        """
        raise NotImplementedError("You should implement is_sane() before running.")

# for decorator
def timemeasure(func):
    def wrapper(*args, **kwargs):
        st = datetime.now()
        func(*args, **kwargs)
        print(f"Time Spent: {(datetime.now() - st).total_seconds():.3f}s")
    return wrapper

