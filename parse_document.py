#!/usr/bin/env python3
"""
Document parsing example using Docling library.
"""

import os
import sys
import argparse
from docling.document_converter import DocumentConverter

def parse_document(source_path):
    """
    Parse a document using Docling and return the results.
    
    Args:
        source_path (str): Path or URL to the document to parse
        
    Returns:
        str: Parsed document in Markdown format
    """
    # Initialize the document converter
    converter = DocumentConverter()
    
    # Convert the document
    result = converter.convert(source_path)
    
    # Export to Markdown
    markdown_content = result.document.export_to_markdown()
    
    return markdown_content

def save_output(content, output_path):
    """
    Save parsed content to a file.
    
    Args:
        content (str): Content to save
        output_path (str): Path where to save the content
    """
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Document parsed and saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Parse documents using Docling")
    parser.add_argument("source", nargs="?", default="https://arxiv.org/pdf/2408.09869", 
                        help="Path or URL to the document to parse (default: Docling technical report)")
    parser.add_argument("-o", "--output", default="output/parsed_document.md",
                        help="Output file path (default: output/parsed_document.md)")
    
    args = parser.parse_args()
    
    source = args.source
    output_file = args.output
    
    print(f"Parsing document: {source}")
    try:
        # Parse the document
        parsed_content = parse_document(source)
        
        # Save the output
        save_output(parsed_content, output_file)
        
        # Print a snippet of the parsed content
        print("\nPreview of parsed content:")
        print(parsed_content[:500] + "..." if len(parsed_content) > 500 else parsed_content)
        
    except Exception as e:
        print(f"Error parsing document: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()