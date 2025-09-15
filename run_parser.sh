#!/bin/bash
# Set environment variables and run the document parser
export HF_HUB_DISABLE_SYMLINKS_WARNING=1
python parse_document.py "$@"