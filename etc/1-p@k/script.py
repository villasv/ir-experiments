import random

import numpy as np
import pandas as pd
import seaborn as sns


class Metric:
    def __init__(self):
        pass

    def _eval(self, r):
        ...

    def __call__(self, r):
        return self._eval(r)


class PatK(Metric):
    def __init__(self, ylim, k=None):
        self._ylim = ylim
        self._k = k

    def _eval(self, r):
        r = np.asfarray(r)
        k = self._k if self._k is not None else r.size
        rk = r[:k]
        return np.sum(rk >= self._ylim) / k


random.seed(42)
patk_nn = PatK(ylim=5)
patk_05 = PatK(ylim=5, k=5)
patk_15 = PatK(ylim=5, k=15)
patk_50 = PatK(ylim=5, k=50)


def gen_ranking(n):
    return np.clip(np.rint(np.random.normal(0, 3, n)), 0, 10)


def main():
    sampling = 100
    linspace = [int(i) for i in np.rint(np.linspace(10 ** 2, 10 ** 4, num=100))]
    rankings = [gen_ranking(n) for n in linspace for _ in range(sampling)]

    df = pd.DataFrame(
        [[r.size, "N", patk_nn(r)] for r in rankings]
        + [[r.size, "05", patk_05(r)] for r in rankings]
        + [[r.size, "50", patk_50(r)] for r in rankings],
        columns=["$N$", "$k$", "$P@k$"],
    )
    sns.lineplot(
        x="$N$", y="$P@k$", hue="$k$", ci="sd", data=df,
    ).get_figure().savefig("patk.png")


if __name__ == "__main__":
    main()
