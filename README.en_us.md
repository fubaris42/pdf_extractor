# PDFExtractor

A high-performance PDF page extraction application with text/regex search, multi-process support, long Windows path support, and both GUI and CLI modes (use core.py directly).

PDFExtractor scans PDF files in a folder, looking for pages containing a specific pattern, and then saves only the matching pages as a new PDF.

## Features

- Extract pages based on text or regular expression
- Regular expression or plain text mode
- Multi-core processing
- Supports Windows paths >260 characters
- Input folder structure is maintained
- Standalone binary (no Python)

## Installation

### Ready-to-Use Binary

1. Go to the GitHub Releases page
2. Download the ZIP file
3. Extract
4. Run:

- `PDFExtractor.exe` (GUI) (create a desktop shortcut if necessary)

### Compile it yourself

1. Windows

```powershell
setup_and_build.ps1
```

1. Linux

```powershell
setup_and_build.sh
```

## How to Use

### GUI

1. Run the application
2. Enter a search pattern or upload a `.txt` file
3. Select the source PDF folder
4. Select the output folder
5. Set options (Regex, Case Sensitive, Recursive)
6. Click **START EXTRACTION**
7. The process log will appear immediately.

### Pattern File (.txt) Format

1. One pattern per line
2. Blank lines are ignored

Example File.txt

```txt
foo
bar
baz
\bINV-\d{6}\b
```

## Regex Flavor

Uses **Python `re` (standard library)**.

- Unicode aware
- Supports lookahead/lookbehind
- Word boundary `\b`
- Case-insensitive default

If **regex is not enabled**, text will be automatically escaped.

## Output Structure

- Each page match → one PDF file
- Folder structure follows input
- File name contains:
- First matched text
- Source PDF name
- Page number

## License

Buy a pack of cigarettes and a cup of coffee.
