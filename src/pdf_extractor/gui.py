#!/usr/bin/env python3
from __future__ import annotations

import sys
import os
import multiprocessing
from pathlib import Path

# Windows-only registry import (safe)
if sys.platform == "win32":
    import winreg
else:
    winreg = None

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLabel,
    QLineEdit,
    QCheckBox,
    QHBoxLayout,
    QTextEdit,
)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QPalette, QColor

# Add 'src' to sys.path if running directly so 'pdf_extractor' package is found
src_path = str(Path(__file__).resolve().parent.parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# ✅ Proper package imports (PyInstaller-safe)
from pdf_extractor.core import PDFExtractor, ExtractionConfig, load_search_inputs


# -----------------------------
# Long Path Helper (The "Chrome" Way)
# -----------------------------
def ensure_long_path(path_str: str) -> str:
    """
    Converts a path to a Windows Extended-Length Path to bypass the 260-char limit.
    """
    if sys.platform != "win32":
        return path_str

    # Get absolute path and resolve any '..'
    p = Path(path_str).resolve()
    abs_path = str(p)

    # Prepend the magic prefix if not already present
    if not abs_path.startswith("\\\\?\\"):
        # If it's a UNC path (network share), handle it specifically
        if abs_path.startswith("\\\\"):
            return "\\\\?\\UNC\\" + abs_path[2:]
        return "\\\\?\\" + abs_path
    return abs_path


# -----------------------------
# Theme handling
# -----------------------------
def is_dark_mode() -> bool:
    if sys.platform.startswith("linux"):
        return True

    if sys.platform == "win32" and winreg:
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(
                registry,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except Exception:
            return True

    return True


def force_dark_palette(app: QApplication) -> None:
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(palette)


# -----------------------------
# Worker thread
# -----------------------------
class ExtractionWorker(QThread):
    finished = pyqtSignal(object)

    def __init__(self, config: ExtractionConfig):
        super().__init__()
        self.config = config

    def run(self) -> None:
        extractor = PDFExtractor(self.config)
        stats = extractor.run()
        self.finished.emit(stats)


# -----------------------------
# Main GUI
# -----------------------------
class PDFExtractGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PDF Extractor (Long-Path Enabled)")
        self.setMinimumSize(850, 650)

        self.active_patterns: list[str] = []
        self.log_file_path: Path | None = None
        self.last_log_size: int = 0
        self.abs_out_dir: str | None = None

        self.apply_theme()
        self.setup_ui()

    def apply_theme(self) -> None:
        dark = is_dark_mode()
        bg = "#1e1e1e" if dark else "#f5f5f5"
        fg = "#ffffff" if dark else "#000000"
        input_bg = "#333333" if dark else "#ffffff"
        log_bg = "#000000" if dark else "#ffffff"
        log_fg = "#00ff00" if dark else "#000000"

        self.setStyleSheet(
            f"""
            QMainWindow, QWidget {{ background-color: {bg}; color: {fg}; }}
            QLineEdit {{ background-color: {input_bg}; color: {fg}; border: 1px solid #555; padding: 5px; }}
            QPushButton {{ background-color: #2980b9; color: white; padding: 8px; border-radius: 4px; font-weight: bold; }}
            QPushButton:hover {{ background-color: #3498db; }}
            QTextEdit {{ background-color: {log_bg}; color: {log_fg}; font-family: monospace; font-size: 11px; border: 2px solid #444; }}
            """
        )

    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>1. Search Patterns</b>"))
        row1 = QHBoxLayout()
        self.pattern_input = QLineEdit()
        self.btn_load_txt = QPushButton("Load .txt")
        self.btn_load_txt.clicked.connect(self.select_pattern_file)
        row1.addWidget(self.pattern_input)
        row1.addWidget(self.btn_load_txt)
        layout.addLayout(row1)

        layout.addWidget(QLabel("<b>2. Source Folder</b>"))
        row2 = QHBoxLayout()
        self.input_path_display = QLineEdit()
        self.btn_browse_input = QPushButton("Browse")
        self.btn_browse_input.clicked.connect(self.select_input_folder)
        row2.addWidget(self.input_path_display)
        row2.addWidget(self.btn_browse_input)
        layout.addLayout(row2)

        layout.addWidget(QLabel("<b>3. Output Folder</b>"))
        row3 = QHBoxLayout()
        self.output_path_input = QLineEdit()
        self.btn_browse_output = QPushButton("Browse")
        self.btn_browse_output.clicked.connect(self.select_output_folder)
        row3.addWidget(self.output_path_input)
        row3.addWidget(self.btn_browse_output)
        layout.addLayout(row3)

        opts = QHBoxLayout()
        self.is_regex = QCheckBox("Regex")
        self.case_sensitive = QCheckBox("Case Sensitive")
        self.recursive = QCheckBox("Recursive")
        self.recursive.setChecked(True)
        opts.addWidget(self.is_regex)
        opts.addWidget(self.case_sensitive)
        opts.addWidget(self.recursive)
        layout.addLayout(opts)

        self.btn_run = QPushButton("START EXTRACTION")
        self.btn_run.clicked.connect(self.start_process)
        layout.addWidget(self.btn_run)

        layout.addWidget(QLabel("<b>Process Log</b>"))
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self.update_log_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_pattern_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Pattern File", "", "Text Files (*.txt)"
        )
        if file_path:
            self.active_patterns = load_search_inputs(file_path)
            self.pattern_input.setText(f"{len(self.active_patterns)} patterns loaded")
            self.pattern_input.setDisabled(True)

    def select_input_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Source")
        if folder:
            self.input_path_display.setText(folder)

            # Get the user's Documents folder (~/Documents)
            docs_path = Path.home() / "Documents"

            # Create a folder name based on the source folder
            folder_name = Path(folder).name + "_extracted"
            default_out = docs_path / folder_name

            # Set the text in the UI (user-friendly view)
            self.output_path_input.setText(str(default_out))

    def select_output_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Destination")
        if folder:
            self.output_path_input.setText(folder)

    # -------------------------
    # Core logic (Updated for Long Paths)
    # -------------------------
    def start_process(self) -> None:
        out_dir_raw = self.output_path_input.text()
        in_dir_raw = self.input_path_display.text()

        if not out_dir_raw or not in_dir_raw:
            return

        # 1. Transform paths to long-path compatible strings immediately
        abs_out = ensure_long_path(out_dir_raw)
        abs_in = ensure_long_path(in_dir_raw)

        self.abs_out_dir = abs_out
        self.log_file_path = Path(abs_out) / "pdf_extractor.log"
        self.last_log_size = 0
        self.log_box.clear()

        # Ensure the log directory exists
        os.makedirs(abs_out, exist_ok=True)

        patterns = self.active_patterns or [self.pattern_input.text()]
        cpu_count = os.cpu_count() or 1
        workers = max(1, int(cpu_count * 0.8))

        config = ExtractionConfig(
            pattern_inputs=patterns,
            use_regex=self.is_regex.isChecked(),
            case_sensitive=self.case_sensitive.isChecked(),
            whole_word=False,
            output_dir=abs_out,  # Passing the prefixed long path
            input_dirs=[abs_in],
            file_patterns=["*.pdf"],
            max_workers=workers,
            log_level="INFO",
            recursive=self.recursive.isChecked(),
            dry_run=False,
        )

        self.btn_run.setEnabled(False)
        self.status_label.setText("Running...")
        self.worker = ExtractionWorker(config)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
        self.log_timer.start(500)

    def update_log_box(self) -> None:
        if self.log_file_path and self.log_file_path.exists():
            try:
                size = self.log_file_path.stat().st_size
                if size > self.last_log_size:
                    with self.log_file_path.open("r", encoding="utf-8") as f:
                        f.seek(self.last_log_size)
                        self.log_box.append(f.read())
                    self.last_log_size = size
            except Exception:
                pass

    def on_finished(self, stats) -> None:
        self.log_timer.stop()
        self.update_log_box()
        self.btn_run.setEnabled(True)
        self.status_label.setText("Done")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    if sys.platform.startswith("linux"):
        app.setStyle("Fusion")
        force_dark_palette(app)
    window = PDFExtractGUI()
    window.show()
    sys.exit(app.exec())
