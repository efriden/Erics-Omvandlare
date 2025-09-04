"""
Pandoc setup utilities for portable executable.

This module handles setting up pandoc path when running as a bundled executable.
"""

import os
import sys
import pypandoc


def setup_pandoc():
    """Set up pandoc path for the bundled executable."""
    if getattr(sys, 'frozen', False):
        # Running as bundled executable
        # In PyInstaller, bundled files are extracted to sys._MEIPASS
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller temporary directory
            application_path = sys._MEIPASS
        else:
            # Fallback to executable directory
            application_path = os.path.dirname(sys.executable)
            
        pandoc_path = os.path.join(application_path, 'pandoc.exe')
        
        if os.path.exists(pandoc_path):
            # Set pandoc path for pypandoc
            os.environ['PYPANDOC_PANDOC'] = pandoc_path
            print(f"Using bundled pandoc: {pandoc_path}")
        else:
            print(f"Warning: Bundled pandoc not found at {pandoc_path}")
            # Try to list what's in the directory for debugging
            try:
                files = os.listdir(application_path)
                pandoc_files = [f for f in files if 'pandoc' in f.lower()]
                if pandoc_files:
                    print(f"Found pandoc-related files: {pandoc_files}")
                else:
                    print(f"No pandoc files found. Directory contains: {files[:10]}...")  # Show first 10 files
            except Exception as e:
                print(f"Could not list directory contents: {e}")
    else:
        print("Running in development mode - using system pandoc")


def get_pandoc_version():
    """Get the version of pandoc being used."""
    try:
        return pypandoc.get_pandoc_version()
    except Exception as e:
        print(f"Could not get pandoc version: {e}")
        return "Unknown"
