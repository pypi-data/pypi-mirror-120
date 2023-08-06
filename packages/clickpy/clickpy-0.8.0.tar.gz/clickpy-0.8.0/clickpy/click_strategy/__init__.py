"""All Clicking Strategies should be placed in this folder."""
from typing import Optional, Protocol, runtime_checkable

import pyautogui
import typer
from clickpy.click_strategy.basic import BasicClickStrategy
from clickpy.click_strategy.natural import NaturalClickStrategy
from clickpy.exception import ClickStrategyNotFound

__all__ = ["auto_click", "click_strategy_factory", "ClickProtocol", "STRATEGIES"]

pyautogui.FAILSAFE = False


@runtime_checkable
class ClickProtocol(Protocol):
    """
    Definition of SupportsClick Protocol.

    Any object with a `__click__()` method can be considered a structural sub-type of
    SupportsClick.
    """

    debug: Optional[bool]

    def __click__(self) -> None:
        """
        Protocol method for the auto_click function.

        Any ClickStrategy class should implement a '__click__' method.
        """

    @classmethod
    def cli_repr(cls) -> str:
        """Return cli/user-friendly string.

        Returns:
            str: simplified cli string for cli.
        """


STRATEGIES: dict[str, type[ClickProtocol]] = {
    BasicClickStrategy.cli_repr(): BasicClickStrategy,
    NaturalClickStrategy.cli_repr(): NaturalClickStrategy,
}


def auto_click(
    click_strategy: ClickProtocol,
) -> None:
    """
    Call `__click__` method of the object passed in.

    Args:
    click_strategy (SupportsClick): Should be a ClickStrategy object.

    Raises:
    TypeError: Error raised if click_strategy is not a structural subtype of SupportClicks,
    """
    if not isinstance(click_strategy, ClickProtocol):
        raise TypeError(f"Argument passed in does not implement" f" {ClickProtocol.__name__}")
    click_strategy.__click__()


def click_strategy_factory(
    click_type: Optional[str] = None, fast: bool = False, debug: bool = False
) -> ClickProtocol:
    """Create ClickStrategy based on cli inputs.

    Raises:
        ClickStrategyNotFound: if click_type arg does not match any known ClickStrategy.

    Returns:
        SupportsClick: ClickStrategy object that implements SupportsClick protocol.
    """
    if debug:
        typer.echo(f"click_type passed into factory func: {click_type!r}")
        if fast:
            pass
            # typer.echo(
            #     f"fast_click flag passed in. default sleep time set to {sleep_time}s, "
            #     "instead of a random interval."
            # )

    # this is the base case, nothing passed in for click_type.
    # empty string should throw exception
    if click_type is None:
        return BasicClickStrategy(debug=debug, fast=fast)

    cleaned_type = click_type.strip().lower()
    if debug:
        typer.echo(f"sanitized click_type={cleaned_type!r}")

    try:
        return STRATEGIES[cleaned_type](debug=debug, fast=fast)  # type: ignore
    except KeyError:
        raise ClickStrategyNotFound()
