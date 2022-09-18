from signal import signal, SIGINT, SIGTERM
from threading import Event

_should_run = True
_exit_event = Event()

def stop() -> None:
    global _should_run
    _should_run = False
    _exit_event.set()
    print("Stop sequence initiated")

def safe_sleep(seconds: float) -> None:
    _exit_event.wait(seconds)

def should_run() -> bool:
    return _should_run

def _sighdlr(*args):
    print("Caught signal, stopping...")
    stop()

def register_signals() -> None:
    signal(SIGINT, _sighdlr)
    signal(SIGTERM, _sighdlr)
