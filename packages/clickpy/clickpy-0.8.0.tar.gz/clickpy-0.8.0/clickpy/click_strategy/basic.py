"""
The first clicker I created.

Gets a random time between 1 second and 3 minutes (in seconds).
"""
from random import randint
from time import sleep

import typer
from pyautogui import click


class BasicClickStrategy:
    """The first, very basic clicking strategy I came up with.

    Before clicking, __click__ will tell the current thread to sleep.
    If self.sleep_time has a value, it will use that as the thread sleep time.
    Else, it will generate a random number between 1 and 180 (3 minutes).
    """

    def __init__(self, **kwargs):
        """Init fields."""
        self.debug = kwargs.get("debug")
        self.sleep_time = 0.5 if kwargs.get("fast") else None
        self._min_sleep_bound: int = 1
        self._max_sleep_bound: int = 180

    def __click__(self) -> None:
        """
        Protocol method defined by SupportsClick.

        Process:
        1. Either use the sleep_time passed into the ctr, or get a random int
        between min_sleep_time and max_sleep_time.
        2. Pause the current thread with above int (in seconds).
        3. call pyautogui.click()
        Optional: print statements if print_debug = True.
        """
        timer = (
            self.sleep_time
            if self.sleep_time
            else float(randint(self._min_sleep_bound, self._max_sleep_bound))
        )

        if self.debug and not self.sleep_time:
            typer.echo(f"Random thread sleep for {timer} seconds.")

        if self.debug:
            typer.echo("Thread sleeping now...")

        sleep(timer)
        click()

        if self.debug:
            typer.echo("... Clicked")

    @classmethod
    def cli_repr(cls) -> str:
        """Return 'basic'."""
        return "basic"
