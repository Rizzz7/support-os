from datetime import datetime
from time import perf_counter
from rich.console import Console
from rich.status import Status

console = Console()

_timers = {}


def _time():
    return datetime.now().strftime("%H:%M:%S")


def info(message: str):
    console.print(
        f"[grey58]{_time()}[/]  [white]INFO[/]      {message}"
    )


def search(message: str):
    console.print(
        f"[grey58]{_time()}[/]  [cyan]SEARCH[/]    {message}"
    )


def read(message: str):
    console.print(
        f"[grey58]{_time()}[/]  [bright_blue]READ[/]      {message}"
    )


def reason(message: str):
    console.print(
        f"[grey58]{_time()}[/]  [magenta]REASON[/]   {message}"
    )


def verify(message: str):
    console.print(
        f"[grey58]{_time()}[/]  [green]VERIFY[/]    {message}"
    )


def error(message: str):
    console.print(
        f"[grey58]{_time()}[/]  [red]ERROR[/]     {message}"
    )


def start_timer(name: str):
    _timers[name] = perf_counter()


def stop_timer(name: str):

    if name not in _timers:
        return 0

    elapsed = perf_counter() - _timers[name]

    del _timers[name]

    return elapsed


class Spinner:

    def __init__(self, message: str):
        self.message = message
        self.status = None

    def __enter__(self):
        self.status = console.status(
            self.message,
            spinner="dots"
        )
        self.status.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.status.stop()