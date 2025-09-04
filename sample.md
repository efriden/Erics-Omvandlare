# Erics-Omvandlare Sample Document

This is a sample Markdown document to demonstrate the conversion capabilities of **Erics-Omvandlare**.

## Features

The application supports conversion between many formats:

- **Markdown** to HTML
- **HTML** to Markdown  
- **Markdown** to PDF
- **Word** documents to Markdown
- And many more!

## Code Example

Here's how to use the DocumentConverter:

```python
from converter import DocumentConverter

converter = DocumentConverter()
html = converter.markdown_to_html("# Hello World")
print(html)
```

## Links and Images

You can also convert documents with links like [Pandoc](https://pandoc.org) and images.

> This is a blockquote showing that complex formatting is preserved during conversion.

### Lists

1. First item
2. Second item
   - Sub item A
   - Sub item B
3. Third item

That's it! Happy converting! 🎉
