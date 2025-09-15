# Usage Guide

## Basic Usage

The simplest way to use this project is to run the main script:

```bash
python parse_document.py
```

This will parse a sample document (by default, the Docling technical report) and save the output as a Markdown file.

## Command Line Interface

After installation, you can use the `parse-doc` command:

```bash
parse-doc
```

## Customizing Document Parsing

### Parsing Local Files

To parse a local document, modify the `source` variable in [parse_document.py](../parse_document.py):

```python
# Replace the URL with a local file path
source = "path/to/your/document.pdf"
```

### Advanced Options

The [advanced_parsing.py](../advanced_parsing.py) script demonstrates more advanced usage patterns:

1. Custom pipeline options for PDF parsing
2. Batch processing of multiple documents
3. Different export formats (Markdown, JSON)

## Configuration Options

### Pipeline Options

You can customize the parsing pipeline by modifying the `PdfPipelineOptions`:

```python
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = False  # Disable OCR
pipeline_options.do_table_structure = True  # Enable table structure detection
```

### Supported Formats

Docling supports various document formats:

- PDF
- DOCX
- PPTX
- XLSX
- HTML
- Images (PNG, JPEG, TIFF)
- And more

## Output Formats

The parsed documents can be exported to multiple formats:

- Markdown (default)
- HTML
- JSON
- DocTags

## Error Handling

The scripts include basic error handling. If a document fails to parse, an error message will be displayed, and the script will continue processing other documents (in batch mode).

## Performance Tips

1. For large batches of documents, consider implementing parallel processing
2. Disable OCR if not needed (`do_ocr = False`)
3. Adjust pipeline options based on your document types
