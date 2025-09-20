#!/usr/bin/env python3

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent / "src"))

from latex_live.cli import main

if __name__ == "__main__":
    main()