#!/usr/bin/env sh

pyinstaller --noconsole --onedir \
            --name "PDFExtractor" \
            --paths "src/pdf_extractor" \
            "src/pdf_extractor/gui.py"