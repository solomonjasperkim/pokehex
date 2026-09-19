"""Launcher for the PokeHex GUI. Run this file directly (works from PyCharm's
Run button too) -- it uses the installed `pokehex` package rather than being
run as a loose script, so relative imports inside the package resolve."""

from pokehex.gui import main

if __name__ == "__main__":
    main()
