from random import randint
from time import sleep

import typer
from pyautogui import click


class NaturalClickStrategy:
    """Click Strategy to replicate a more natural clicking pattern."""

    def __init__(self, **kwargs):
        """Init fields."""
        self.debug = kwargs.get("debug")
        self._min_sleep_bound = 5
        self._max_sleep_bound = 60
        self.wait_times = [1.0, 1.0, 2.5, randint(self._min_sleep_bound, self._max_sleep_bound)]

    def __click__(self):
        """Protocol method defined by SupportsClick.

        Process:
        Define a list of 'wait times', i.e. time in between clicks.
        In a loop, click mouse then sleep that iterations wait time.
        At the end, get a random time between min and max bounds.
        """
        for time in self.wait_times:
            if self.debug:
                typer.echo(f"Waiting for {time} sec ...")

            sleep(time)
            click()

            if self.debug:
                typer.echo("... Clicked")

    @classmethod
    def cli_repr(cls) -> str:
        """Return 'natural'."""
        return "natural"
