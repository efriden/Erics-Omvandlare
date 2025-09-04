#!/usr/bin/env python3
"""
Test script to validate the portable executable functionality.
This can be run to test that all components work correctly.
"""

import sys
import os
import tempfile

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pandoc_setup import setup_pandoc, get_pandoc_version
from converter import DocumentConverter

def test_pandoc_setup():
    """Test pandoc setup functionality."""
    print("Testing pandoc setup...")
    setup_pandoc()
    
    version = get_pandoc_version()
    print(f"Pandoc version: {version}")
    
    if version == "Unknown":
        print("❌ Failed to get pandoc version")
        return False
    else:
        print("✅ Pandoc setup successful")
        return True

def test_converter():
    """Test document conversion functionality."""
    print("\nTesting document converter...")
    
    try:
        converter = DocumentConverter()
        
        # Test markdown to HTML conversion
        test_markdown = "# Test Document\n\nThis is a **test** with some *emphasis*.\n\n- Item 1\n- Item 2"
        
        html_result = converter.markdown_to_html(test_markdown)
        print("✅ Markdown to HTML conversion successful")
        print(f"Result preview: {html_result[:100]}...")
        
        # Test HTML to markdown conversion
        test_html = "<h1>Hello</h1><p>This is <strong>HTML</strong> content.</p>"
        md_result = converter.html_to_markdown(test_html)
        print("✅ HTML to Markdown conversion successful")
        print(f"Result: {md_result}")
        
        # Test file conversion to a temporary DOCX file
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
            temp_path = temp_file.name
            
        try:
            converter.convert_text(test_markdown, 'docx', 'markdown', output_file=temp_path)
            if os.path.exists(temp_path):
                file_size = os.path.getsize(temp_path)
                print(f"✅ DOCX conversion successful (file size: {file_size} bytes)")
                os.unlink(temp_path)  # Clean up
                return True
            else:
                print("❌ DOCX file was not created")
                return False
        except Exception as e:
            print(f"❌ DOCX conversion failed: {e}")
            if os.path.exists(temp_path):
                os.unlink(temp_path)  # Clean up
            return False
            
    except Exception as e:
        print(f"❌ Converter test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Erics-Omvandlare Components")
    print("=" * 50)
    
    pandoc_ok = test_pandoc_setup()
    converter_ok = test_converter()
    
    print("\n" + "=" * 50)
    if pandoc_ok and converter_ok:
        print("🎉 All tests passed! The portable executable should work correctly.")
    else:
        print("❌ Some tests failed. Check the output above.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
