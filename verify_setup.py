#!/usr/bin/env python3
"""
Script to verify that the Docling parser setup is working correctly.
"""

import sys
import importlib.util

def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"ERROR: Python 3.11 or higher is required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✓ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_package_installed(package_name):
    """Check if a package is installed."""
    print(f"Checking if {package_name} is installed...")
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is not None:
            print(f"✓ {package_name} is installed")
            return True
        else:
            print(f"✗ {package_name} is not installed")
            return False
    except ImportError:
        print(f"✗ {package_name} is not installed")
        return False

def test_docling_import():
    """Test importing Docling components."""
    print("Testing Docling imports...")
    try:
        from docling.document_converter import DocumentConverter
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        print("✓ Docling components imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import Docling components: {e}")
        return False
    except Exception as e:
        print(f"✗ Error importing Docling components: {e}")
        return False

def main():
    """Main verification function."""
    print("Verifying Docling Parser setup...\n")
    
    checks = [
        check_python_version,
        lambda: check_package_installed("docling"),
        test_docling_import
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
        print()  # Add spacing between checks
    
    if all_passed:
        print("✓ All checks passed! Your setup is ready to use.")
        print("\nNext steps:")
        print("1. Try parsing a document: python parse_document.py")
        print("2. For advanced usage: python advanced_parsing.py")
        print("3. Run tests: pytest")
    else:
        print("✗ Some checks failed. Please review the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()