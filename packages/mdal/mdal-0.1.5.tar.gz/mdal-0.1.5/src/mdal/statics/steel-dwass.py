# -*- coding: utf-8 -*-
import scikit_posthocs as sp


# 正規性がないデータ、かつ、複数群同士をすべて比較したいときに使う検定
def test(data):
    return sp.posthoc_dscf(data)
