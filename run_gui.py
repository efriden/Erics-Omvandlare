#!/usr/bin/env python3
"""
Launcher script for Erics-Omvandlare GUI application.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Setup pandoc for bundled executable
from pandoc_setup import setup_pandoc
setup_pandoc()

# Import and run the GUI
from gui import main

if __name__ == "__main__":
    main()
