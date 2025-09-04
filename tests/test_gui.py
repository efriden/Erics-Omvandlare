"""Tests for the GUI module."""

import sys
import os
import pytest

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_gui_imports():
    """Test that GUI module can be imported without errors."""
    try:
        from gui import OmvandlareGUI
        assert OmvandlareGUI is not None
    except ImportError as e:
        pytest.fail(f"Failed to import GUI module: {e}")


def test_gui_class_creation():
    """Test that OmvandlareGUI class can be instantiated."""
    # Note: This test doesn't actually create the GUI window to avoid display issues
    # in testing environments
    try:
        from gui import OmvandlareGUI
        # Just verify the class exists and can be referenced
        assert hasattr(OmvandlareGUI, '__init__')
        assert hasattr(OmvandlareGUI, 'setup_gui')
        assert hasattr(OmvandlareGUI, 'export_to_docx')  # Only DOCX export now
        assert hasattr(OmvandlareGUI, 'clear_text')
        # PDF export has been removed
        assert not hasattr(OmvandlareGUI, 'export_to_pdf')
    except Exception as e:
        pytest.fail(f"Failed to verify GUI class: {e}")


def test_gui_filename_generation():
    """Test filename generation method."""
    try:
        from gui import OmvandlareGUI
        import tkinter as tk
        
        # Create a minimal GUI instance for testing
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        gui = OmvandlareGUI.__new__(OmvandlareGUI)  # Create without calling __init__
        
        # Test filename generation
        pdf_filename = gui.generate_filename("pdf")
        docx_filename = gui.generate_filename("docx")
        
        assert pdf_filename.endswith(".pdf")
        assert docx_filename.endswith(".docx")
        assert "converted_document_" in pdf_filename
        assert "converted_document_" in docx_filename
        
        # Verify the format includes timestamp
        import re
        timestamp_pattern = r"\d{8}_\d{6}"
        assert re.search(timestamp_pattern, pdf_filename), f"PDF filename should contain timestamp: {pdf_filename}"
        assert re.search(timestamp_pattern, docx_filename), f"DOCX filename should contain timestamp: {docx_filename}"
        
        root.destroy()
        
    except Exception as e:
        pytest.fail(f"Failed to test filename generation: {e}")
