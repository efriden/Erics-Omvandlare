#!/usr/bin/env python3
"""
Erics-Omvandlare - Conversion utility application

Main entry point for the application.
"""

import pypandoc
import os
from converter import DocumentConverter
from pandoc_setup import setup_pandoc, get_pandoc_version

def test_pandoc_installation():
    """Test if pypandoc and pandoc are properly installed."""
    try:
        # Check pypandoc version
        print(f"pypandoc version: {pypandoc.__version__}")
        print(f"pandoc version: {get_pandoc_version()}")
        
        # Test basic conversion
        test_markdown = "# Hello World\nThis is a **test** document."
        html_output = pypandoc.convert_text(test_markdown, 'html', format='md')
        print("✓ pypandoc is working correctly!")
        print("Sample conversion (Markdown to HTML):")
        print(html_output)
        return True
    except Exception as e:
        print(f"✗ Error with pypandoc: {e}")
        print("You may need to install pandoc separately.")
        return False

def main():
    """Main function to start the application."""
    # Ensure the bundled pandoc is used when frozen
    setup_pandoc()

    print("Welcome to Erics-Omvandlare!")
    print("This is a conversion utility application using Pandoc.")
    print("\nTesting pypandoc installation...")
    
    if test_pandoc_installation():
        print("\n🎉 Ready to start converting documents!")
        
        # Demonstrate converter functionality
        print("\n--- Demonstrating DocumentConverter ---")
        converter = DocumentConverter()
        
        # Show supported formats
        formats = converter.get_supported_formats()
        print(f"Supported input formats: {len(formats['input'])} formats")
        print(f"Supported output formats: {len(formats['output'])} formats")
        
        # Example conversions
        sample_markdown = "# Erics-Omvandlare\n\nThis is a **powerful** conversion tool that supports:\n\n- Markdown to HTML\n- HTML to Markdown\n- And many more formats!"
        
        print("\nExample: Markdown to HTML conversion:")
        html_result = converter.markdown_to_html(sample_markdown)
        print(html_result)
        
        print("\nExample: HTML to Markdown conversion:")
        html_input = "<h2>Hello</h2><p>This is <em>HTML</em> content.</p>"
        md_result = converter.html_to_markdown(html_input)
        print(md_result)
        
    else:
        print("\n⚠️  Please install pandoc to use all features.")
        print("Visit: https://pandoc.org/installing.html")

if __name__ == "__main__":
    main()
