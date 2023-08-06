# -*- coding: utf-8 -*-

import scipy.stats as stats
import matplotlib.pyplot as plt


def __statics_test(sample):
    # サンプル数の条件判断は理解できていない
    # TODO: 追加の判定が必要である
    if len(sample) < 1000:
        s, p = stats.shapiro(sample)
    else:
        s, p = stats.kstest(sample, "norm")

    return s, p


def __judge(p_value: float):
    if p_value < 0.05:
        return False
    else:
        return True


def is_normality(sample):
    _, p = __statics_test(sample)

    return __judge(p)


def show_normality(sample):
    s, p = __statics_test(sample)

    if __judge(p):
        print("サンプルは正規分布に従っています。")
    else:
        print("サンプルは正規分布に従っていません。")

    print(f"統計値: {s}")
    print(f"p 値: {p}")
    stats.probplot(sample, dist="norm", plot=plt)
    plt.show()
