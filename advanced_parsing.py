import os
import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.format_option import PdfFormatOption

def parse_pdf_with_options(pdf_path):
    """
    Parse a PDF with custom pipeline options.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        tuple: (markdown_content, json_content)
    """
    # Configure pipeline options
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False  # Disable OCR if not needed
    pipeline_options.do_table_structure = True  # Enable table structure
    
    # Create format option with pipeline options
    pdf_format_option = PdfFormatOption(pipeline_options=pipeline_options)
    
    # Initialize converter with specific format option
    converter = DocumentConverter(format_options={InputFormat.PDF: pdf_format_option})
    
    # Convert the document
    result = converter.convert(pdf_path)
    
    # Export to different formats
    markdown_content = result.document.export_to_markdown()
    json_content = result.document.export_to_dict()
    
    return markdown_content, json_content

def parse_single_document(doc_path):
    """
    Parse a single document and return the result.
    
    Args:
        doc_path (str): Path to the document
        
    Returns:
        dict: Parsing result
    """
    try:
        converter = DocumentConverter()
        result = converter.convert(doc_path)
        return {
            'source': doc_path,
            'markdown': result.document.export_to_markdown(),
            'json': result.document.export_to_dict(),
            'success': True
        }
    except Exception as e:
        return {
            'source': doc_path,
            'error': str(e),
            'success': False
        }

def parse_multiple_documents_sequential(doc_paths):
    """
    Parse multiple documents sequentially.
    
    Args:
        doc_paths (list): List of document paths
        
    Returns:
        list: List of parsed documents
    """
    results = []
    
    for path in doc_paths:
        result = parse_single_document(path)
        results.append(result)
        if result['success']:
            print(f"Successfully parsed: {path}")
        else:
            print(f"Error parsing {path}: {result['error']}")
    
    return results

def parse_multiple_documents_concurrent(doc_paths, max_workers=4):
    """
    Parse multiple documents concurrently using ThreadPoolExecutor.
    
    Args:
        doc_paths (list): List of document paths
        max_workers (int): Maximum number of concurrent threads
        
    Returns:
        list: List of parsed documents
    """
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all parsing tasks
        future_to_path = {
            executor.submit(parse_single_document, path): path 
            for path in doc_paths
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                result = future.result()
                results.append(result)
                if result['success']:
                    print(f"Successfully parsed: {path}")
                else:
                    print(f"Error parsing {path}: {result['error']}")
            except Exception as e:
                error_result = {
                    'source': path,
                    'error': str(e),
                    'success': False
                }
                results.append(error_result)
                print(f"Error parsing {path}: {e}")
    
    return results

def save_results(results, output_dir="output"):
    """
    Save parsing results to files.
    
    Args:
        results (list): List of parsing results
        output_dir (str): Directory to save results
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for i, result in enumerate(results):
        if not result['success']:
            continue
            
        base_name = os.path.basename(result['source'])
        name_without_ext = os.path.splitext(base_name)[0]
        
        # Save Markdown
        md_path = os.path.join(output_dir, f"{name_without_ext}.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(result['markdown'])
        
        # Save JSON
        json_path = os.path.join(output_dir, f"{name_without_ext}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            import json
            json.dump(result['json'], f, indent=2, ensure_ascii=False)
        
        print(f"Saved results for {result['source']}")

def main():
    parser = argparse.ArgumentParser(description="Advanced Docling parsing examples")
    parser.add_argument("documents", nargs="*", help="Paths to documents to parse")
    parser.add_argument("-o", "--output-dir", default="output", help="Output directory")
    parser.add_argument("--pdf-options", action="store_true", help="Use advanced PDF options")
    parser.add_argument("--concurrent", action="store_true", help="Use concurrent parsing")
    parser.add_argument("--max-workers", type=int, default=4, help="Maximum number of concurrent workers")
    
    args = parser.parse_args()
    
    if not args.documents:
        print("No documents provided. Please specify document paths to parse.")
        print("Usage: python advanced_parsing.py doc1.pdf doc2.docx")
        sys.exit(1)
    
    print("Advanced Docling parsing examples")
    
    if args.pdf_options and len(args.documents) == 1 and args.documents[0].endswith('.pdf'):
        # Parse single PDF with custom options
        pdf_path = args.documents[0]
        print(f"Parsing PDF with custom options: {pdf_path}")
        try:
            markdown, json_data = parse_pdf_with_options(pdf_path)
            
            # Save results
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            md_path = os.path.join(args.output_dir, f"{base_name}_advanced.md")
            json_path = os.path.join(args.output_dir, f"{base_name}_advanced.json")
            
            os.makedirs(args.output_dir, exist_ok=True)
            
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            
            with open(json_path, 'w', encoding='utf-8') as f:
                import json
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            print(f"Saved advanced parsing results to {args.output_dir}")
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            sys.exit(1)
    else:
        # Parse multiple documents
        print(f"Parsing {len(args.documents)} documents...")
        
        start_time = time.time()
        
        if args.concurrent:
            print(f"Using concurrent parsing with {args.max_workers} workers...")
            results = parse_multiple_documents_concurrent(args.documents, args.max_workers)
        else:
            print("Using sequential parsing...")
            results = parse_multiple_documents_sequential(args.documents)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        save_results(results, args.output_dir)
        print(f"Saved all results to {args.output_dir}")
        print(f"Parsing completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()