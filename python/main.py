#!/usr/bin/env python3
"""
Convenience launcher.

Run directly without installing the package:

    python main.py "2x^3 - 3x^2 + 5"
    python main.py --interactive
    python main.py --examples

This simply calls the same high-level API as the installed package.
"""

import sys
from pathlib import Path

# Ensure we can import from src/ when running from project root
sys.path.insert(0, str(Path(__file__).parent / "src"))

from polynomial_explorer.__main__ import main

if __name__ == "__main__":
    main()
