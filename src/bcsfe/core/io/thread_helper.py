from typing import Callable, Any, Optional
import threading


class Thread:
    def __init__(self, name: str, target: Callable[..., Any], args: Any):
        self.name = name
        self.target = target
        self.args = args
        self._thread: Optional[threading.Thread] = None

    def start(self):
        self._thread = threading.Thread(
            target=self.target, args=self.args, name=self.name
        )
        self._thread.start()

    def join(self):
        if self._thread is not None:
            self._thread.join()

    def is_alive(self) -> bool:
        if self._thread is not None:
            return self._thread.is_alive()
        else:
            return False

    @staticmethod
    def run(name: str, target: Callable[..., None], args: Any):
        thread = Thread(name, target, args)
        thread.start()
        return thread


def run_many_helper(funcs: list[Callable[..., Any]], *args: list[Any]):
    for i in range(len(funcs)):
        args_ = args[i]
        funcs[i](*args_)
    return


def run_many(funcs: list[Callable[..., Any]], args: Any = None, max_threads: int = 32):
    chunk_size = len(funcs) // max_threads
    if chunk_size == 0:
        chunk_size = 1
    callable_chunks: list[list[Callable[..., Any]]] = []
    args_chunks: list[list[Any]] = []
    for i in range(0, len(funcs), chunk_size):
        callable_chunks.append(funcs[i : i + chunk_size])
        args_chunks.append(args[i : i + chunk_size])

    threads: list[Thread] = []
    for i in range(len(callable_chunks)):
        args_ = args_chunks[i]
        if args is None:
            args_ = []

        threads.append(
            Thread.run("run_many_helper", run_many_helper, (callable_chunks[i], *args_))
        )

    for thread in threads:
        thread.join()

    return threads