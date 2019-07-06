def ta_rule_ge_direction(list):
    if list[0] > list[len(list) - 1]:
        return "BUY"
    elif list[0] == list[len(list) - 1]:
        return "HOLD"
    else:
        return "SELL"


def ta_rule_ge_value(sma, ema, wma, rsi):
    ta_value = 0.5
    if sma > ema:
        if rsi > 70:
            ta_value += 0.4
        elif rsi > 50:
            ta_value += 0.2
        elif rsi > 30:
            ta_value += 0.05
        else:
            ta_value -= 0.35
    elif sma < ema:
        if rsi > 70:
            ta_value -= 0.35
        elif rsi > 50:
            ta_value += 0.05
        elif rsi > 30:
            ta_value += 0.2
        else:
            ta_value += 0.4

    return ta_value
