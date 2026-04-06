"""Project-specific CLI commands.

Add custom CLI commands here as public functions. All public functions are
automatically discovered and registered as CLI commands.
"""


def run() -> None:
    """Run the notty game."""
    from notty.main import main  # noqa: PLC0415

    main()
