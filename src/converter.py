"""
Conversion utilities using pypandoc.

This module provides various document conversion functions.
"""

import pypandoc
import os
from typing import Optional


class DocumentConverter:
    """A class for converting between different document formats using pypandoc."""
    
    def __init__(self):
        """Initialize the converter."""
        self.supported_formats = {
            'input': pypandoc.get_pandoc_formats()[0],
            'output': pypandoc.get_pandoc_formats()[1]
        }
    
    def convert_file(self, input_file: str, output_format: str, 
                     output_file: Optional[str] = None) -> str:
        """
        Convert a file from one format to another.
        
        Args:
            input_file: Path to the input file
            output_format: Target format (e.g., 'html', 'pdf', 'docx')
            output_file: Optional output file path
            
        Returns:
            Converted content as string or output file path
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        if output_file:
            pypandoc.convert_file(input_file, output_format, outputfile=output_file)
            return output_file
        else:
            return pypandoc.convert_file(input_file, output_format)
    
    def convert_text(self, text: str, output_format: str, 
                     input_format: str = 'markdown', output_file: Optional[str] = None) -> str:
        """
        Convert text from one format to another.
        
        Args:
            text: Input text to convert
            output_format: Target format
            input_format: Source format (default: markdown)
            output_file: Optional output file path
            
        Returns:
            Converted text or output file path
        """
        if output_file:
            pypandoc.convert_text(text, output_format, format=input_format, outputfile=output_file)
            return output_file
        else:
            return pypandoc.convert_text(text, output_format, format=input_format)
    
    def get_supported_formats(self) -> dict:
        """Get list of supported input and output formats."""
        return self.supported_formats
    
    def markdown_to_html(self, markdown_text: str) -> str:
        """Convert Markdown to HTML."""
        return self.convert_text(markdown_text, 'html', 'markdown')
    
    def markdown_to_pdf(self, markdown_text: str, output_file: str) -> str:
        """Convert Markdown to PDF file."""
        pypandoc.convert_text(markdown_text, 'pdf', format='markdown', 
                             outputfile=output_file)
        return output_file
    
    def html_to_markdown(self, html_text: str) -> str:
        """Convert HTML to Markdown."""
        return self.convert_text(html_text, 'markdown', 'html')
