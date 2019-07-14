from queue import Queue
from typing import Any

import rx
from rx import operators as ops, Observable
from rx.core import Observer
from rx.core.abc import Scheduler
from rx.disposable import Disposable
from rx.subject import Subject

from data.data_models import TickWindow
from ta_lib.ta_methods import sma


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


def __sma__(stream, sma_size, skip=1):
    return stream.pipe(
        ops.map(lambda window: window.close),
        _windowing(sma_size + 1, skip),
        ops.filter(lambda w: w is not None),
        ops.map(lambda wlist: sma(wlist, sma_size))
    )


class TAnalyser:

    def __init__(self, window_size):
        self.window_size = window_size
        self.tick_stream_subject = rx.subject.Subject()
        self.window_stream = self.tick_stream_subject.pipe(
            ops.buffer_with_time(self.window_size+1),
            ops.map(lambda tick_list: TickWindow.from_tick_list(tick_list)),
            ops.filter(lambda w: w is not None)
        )

        __sma__(self.window_stream, 5, 1).subscribe_(print)

    def on_next(self, tick):
        self.tick_stream_subject.on_next(tick)
