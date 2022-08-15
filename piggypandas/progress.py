from typing import Callable, Optional, Any
import sys


ProgressCallback = Optional[Callable[[int], Any]]


class Progress(object):

    def __init__(self, total: int, on_progress: ProgressCallback, on_exit: ProgressCallback):
        self._total: int = total
        self._progress: int = 0
        self._progress_percent: int = 0
        self._on_progress = on_progress
        self._on_exit = on_exit

    def reset(self):
        self._progress = 0
        self._progress_percent = 0

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        if self._on_exit:
            self._on_exit(self._progress_percent)

    def tick(self, size: int):
        self._progress += size
        if self._total > 0:
            progress_percent = int((self._progress * 100) / self._total)
            if progress_percent != self._progress_percent:
                self._progress_percent = progress_percent
                if self._on_progress:
                    self._on_progress(self._progress_percent)


class ConsoleProgress(Progress):

    def __init__(self, total: int, use_stderr: bool = False):
        stream = sys.stderr if use_stderr else sys.stdout
        super().__init__(total,
                         on_progress=lambda n: stream.write(f"\r{n}%"),
                         on_exit=lambda _: stream.write("\n")
                         )
