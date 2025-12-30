#!/usr/bin/env sh
set -e

pyinstaller \
  --onedir \
  --windowed \
  --name PDFExtractorLinux \
  --collect-submodules PyQt6 \
  --collect-data PyQt6 \
  --hidden-import fitz \
  --paths src \
  src/pdf_extractor/gui.py