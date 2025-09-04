"""Tests for the main module and converter functionality."""

import sys
import os
import pytest

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import main
from converter import DocumentConverter


def test_main_output(capfd):
    """Test that main function produces expected output."""
    main()
    captured = capfd.readouterr()
    assert "Welcome to Erics-Omvandlare!" in captured.out
    assert "conversion utility application" in captured.out


def test_document_converter_initialization():
    """Test DocumentConverter can be initialized."""
    converter = DocumentConverter()
    assert converter is not None
    formats = converter.get_supported_formats()
    assert 'input' in formats
    assert 'output' in formats


def test_markdown_to_html_conversion():
    """Test basic markdown to HTML conversion."""
    converter = DocumentConverter()
    markdown = "# Test\n\nThis is **bold** text."
    html = converter.markdown_to_html(markdown)
    assert "<h1" in html
    assert "<strong>bold</strong>" in html


def test_html_to_markdown_conversion():
    """Test basic HTML to markdown conversion."""
    converter = DocumentConverter()
    html = "<h1>Test</h1><p>This is <strong>bold</strong> text.</p>"
    markdown = converter.html_to_markdown(html)
    assert "# Test" in markdown
    assert "**bold**" in markdown
