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
from ta_lib.ta_methods import sma


def _time_windowing(time):
    data_list = []

    vars = {
        "start_time": None
    }

    def map(source: Observable) -> Observable:

        def subscribe(obv: Observer, scheduler: Scheduler = None) -> Disposable:
            def on_next(value: Any) -> None:
                try:
                    # print(value)
                    data_list.append(value)
                    result = None

                    current_time = datetime.datetime.fromtimestamp(value.epoch)
                    # _, _, _, _, min_2, sec_2, _, _, _ = current_time.timetuple()

                    if vars['start_time'] is None:
                        vars['start_time'] = datetime.datetime.fromtimestamp(value.epoch)

                    window_begin_time = vars['start_time']
                    # _, _, _, _, min_1, sec_1, _, _, _ = window_begin_time.timetuple()

                    time_sec_diff = current_time - window_begin_time
                    time_sec_diff = time_sec_diff.seconds

                    # min_diff = min_2 - min_1
                    # sec_diff = sec_2 - sec_1
                    # print(time_sec_diff, time, time_sec_diff >= time)

                    if time_sec_diff >= time:
                        result = list(data_list)
                        data_list.clear()
                        vars['start_time'] = None
                        # print(len(data_list))

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


def create_stream_ta(window_size):
    tick_stream_subject = rx.subject.Subject()
    tick_stream_obs = tick_stream_subject.pipe(
        _time_windowing(window_size),
        ops.filter(lambda list: list),
        ops.map(lambda tick_list: TickWindow.from_tick_list(tick_list)),
        ops.filter(lambda w: w is not None),
        ops.map(lambda window: [window.epoch, window.close]),
        _windowing(20),
        ops.filter(lambda w: w is not None),
        ops.map(lambda wlist: np.array(wlist))
    )
    return tick_stream_subject, tick_stream_obs


class TAnalyser:
    ta_subscribers = []

    def __init__(self, symbol, window_size):
        sma_5_sub, sma_5_obs = create_stream_ta(window_size=2)
        sma_5_obs = sma_5_obs.pipe(
            ops.map(lambda wlist: TIData(name="SMA", time_interval=5, epoch=wlist[:1, 0], data=sma(wlist[:, 1], 5),
                                         symbol=symbol))
        )
        self.ta_subscribers.append(sma_5_sub)

        sma_14_sub, sma_14_obs = create_stream_ta(window_size=2)
        sma_14_obs = sma_14_obs.pipe(
            ops.map(
                lambda wlist: TIData(name="SMA", time_interval=14, epoch=wlist[:1, 0], data=sma(wlist[:, 1], 14),
                                     symbol=symbol))
        )
        self.ta_subscribers.append(sma_14_sub)
        #
        sma_5_obs.subscribe_(on_next=lambda p: print(f"5 {p}"))
        sma_14_obs.subscribe_(on_next=lambda p: print(f"14 {p}"))

    def on_next(self, tick):
        # rx.from_iterable(self.ta_subscribers).subscribe_(on_next=lambda s: s.on_next(tick))
        rx.from_iterable(self.ta_subscribers).subscribe_(on_next=lambda s: s.on_next(tick))
