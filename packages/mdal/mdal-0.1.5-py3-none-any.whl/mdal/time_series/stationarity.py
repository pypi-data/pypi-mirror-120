# -*- coding: utf-8 -*-
from pmdarima.arima import ADFTest, KPSSTest, PPTest

def test(time_series):
    p_value_s = []
    result_s = []
    for test in [ADFTest(), KPSSTest(), PPTest()]:
        p_value, result = test.should_diff(time_series)
        p_value_s.append(p_value)

        if result:
            result_s.append("not stationarity.")
        else:
            result_s.append("stationarity.")

    return pd.DataFrame({
        "test_name": ["ADF", "KPSS", "PP"],
        "p-value": p_value_s,
        "result": result_s
    })