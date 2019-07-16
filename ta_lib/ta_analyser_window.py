import datetime
from queue import Queue
from typing import Any

import numpy as np
import rx
from rx import operators as ops, Observable
from rx.core import Observer
from rx.core.abc import Scheduler
from rx.disposable import Disposable
from rx.subject import Subject

from data.data_models import TickWindow, TIData
from ta_lib.ta_methods import sma, rsi, ema
from utils import round_seconds


def _window_filter():
    data_list = []

    vars = {
        "start_time": None
    }

    def map(source: Observable) -> Observable:

        def subscribe(obv: Observer, scheduler: Scheduler = None) -> Disposable:
            def on_next(value: TickWindow) -> None:
                try:
                    result = None
                    if vars['start_time'] is None:
                        vars['start_time'] = value.epoch
                    else:
                        if vars['start_time'] == value.epoch:
                            result = value
                            vars['start_time'] = None

                            # result = value
                except Exception as err:  # pylint: disable=broad-except
                    obv.on_error(err)
                else:
                    obv.on_next(result)

            return source.subscribe_(on_next, obv.on_error, obv.on_completed, scheduler)

        return Observable(subscribe)

    return map


def _windowing(window_length, skip=1):
    _window_length = window_length

    window_que = Queue(maxsize=window_length)

    def map(source: Observable) -> Observable:

        def subscribe(obv: Observer, scheduler: Scheduler = None) -> Disposable:
            def on_next(value: Any) -> None:
                try:
                    window_que.put(value)
                    result = None
                    if window_que.full():
                        result = list(window_que.queue)
                        for i in range(skip):
                            window_que.get()
                    # window_que.put()

                    # result = value
                except Exception as err:  # pylint: disable=broad-except
                    obv.on_error(err)
                else:
                    obv.on_next(result)

            return source.subscribe_(on_next, obv.on_error, obv.on_completed, scheduler)

        return Observable(subscribe)

    return map


def test(a):
    def print_a(b):
        # print(f"--{a}--")
        # print(b)
        # print("-----")
        return b

    return print_a


def to_array(wlist):
    try:
        return np.array(wlist)
    except Exception as err:
        print(err)
    return None


def create_stream_ta(window_time):
    tick_stream_subject = rx.subject.Subject()
    tick_stream_obs = tick_stream_subject.pipe(
        _window_filter(),
        ops.filter(lambda w: w),
        ops.map(test(0)),
        ops.map(lambda window: [window.epoch, window.close]),
        ops.map(test(1)),
        _windowing(window_time),
        ops.filter(lambda w: w),
        ops.map(test(2)),
        ops.map(to_array),
        ops.map(test(3)),
    )
    return tick_stream_subject, tick_stream_obs


def get_symbol(wlist):
    return wlist[:1, 2][0]


class TAnalyserWidow:
    ta_subscribers = []

    def __init__(self, window_time, symbol):
        self.window_time = window_time
        self.symbol = symbol
        try:
            sma_5_sub, sma_5_obs = create_stream_ta(window_time=window_time)
            sma_5_obs = sma_5_obs.pipe(
                ops.map(lambda wlist: TIData(name="SMA", time_interval=5, epoch=wlist[:1, 0][0],
                                             data=sma(np.array(wlist[:, 1]).astype(np.float), 5),
                                             symbol=self.symbol)),

                # ops.map(test(4))
            )
            self.ta_subscribers.append(sma_5_sub)

            ema_14_sub, ema_14_obs = create_stream_ta(window_time=window_time)
            ema_14_obs = ema_14_obs.pipe(
                ops.map(
                    lambda wlist: TIData(name="EMA", time_interval=14, epoch=wlist[:1, 0][0],
                                         data=sma(np.array(wlist[:, 1]).astype(np.float), 14),
                                         symbol=self.symbol)),

                # ops.map(test(5))
            )
            self.ta_subscribers.append(ema_14_sub)
            #

            rsi_14_sub, rsi_14_obs = create_stream_ta(window_time=window_time)
            rsi_14_obs = rsi_14_obs.pipe(
                ops.map(
                    lambda wlist: TIData(name="RSI", time_interval=7, epoch=wlist[:1, 0][0],
                                         data=rsi(np.array(wlist[:, 1]).astype(np.float), 7),
                                         symbol=self.symbol)),

                # ops.map(test(6))
            )
            self.ta_subscribers.append(rsi_14_sub)

            self.ta_result = rx.merge(sma_5_obs, ema_14_obs, rsi_14_obs)
        except Exception as err:
            print(err)

    def on_next(self, tick):
        # rx.from_iterable(self.ta_subscribers).subscribe_(on_next=lambda s: s.on_next(tick))
        rx.from_iterable(self.ta_subscribers).subscribe_(on_next=lambda s: s.on_next(tick))

    def __str__(self) -> str:
        return f"{self.symbol}-{self.window_time}"
