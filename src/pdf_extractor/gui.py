import sys
import os
import multiprocessing
import winreg
from pathlib import Path
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
    QProgressBar,
    QHBoxLayout,
    QTextEdit,
)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt

# Import your existing logic
from .core import PDFExtractor, ExtractionConfig, load_search_inputs


def is_dark_mode():
    """Checks Windows Registry for system theme preference."""
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(
            registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return value == 0
    except Exception:
        return False


class ExtractionWorker(QThread):
    finished = pyqtSignal(object)

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        extractor = PDFExtractor(self.config)
        stats = extractor.run()
        self.finished.emit(stats)


class PDFExtractGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Extractor Pro")
        self.setMinimumSize(850, 650)
        self.active_patterns = []
        self.log_file_path = None
        self.last_log_size = 0

        # Apply Theme before UI setup
        self.apply_theme()
        self.setup_ui()

    def apply_theme(self):
        """Sets colors based on Windows System Theme."""
        dark = is_dark_mode()
        if dark:
            # Dark Theme Palette
            self.bg_color = "#1e1e1e"
            self.text_color = "#ffffff"
            self.log_bg = "#000000"
            self.log_text = "#00ff00"  # Classic Matrix/Terminal Green for dark mode
            self.input_bg = "#333333"
        else:
            # Light Theme Palette
            self.bg_color = "#f5f5f5"
            self.text_color = "#000000"
            self.log_bg = "#ffffff"
            self.log_text = "#000000"
            self.input_bg = "#ffffff"

        self.setStyleSheet(
            f"""
            QMainWindow, QWidget {{ background-color: {self.bg_color}; color: {self.text_color}; }}
            QLineEdit {{ background-color: {self.input_bg}; color: {self.text_color}; border: 1px solid #555; padding: 5px; }}
            QPushButton {{ background-color: #2980b9; color: white; padding: 8px; border-radius: 4px; font-weight: bold; }}
            QPushButton:hover {{ background-color: #3498db; }}
            QTextEdit {{
                background-color: {self.log_bg}; 
                color: {self.log_text}; 
                font-family: 'Consolas', 'Monaco', monospace; 
                font-size: 11px;
                border: 2px solid #444;
            }}
        """
        )

    def setup_ui(self):
        layout = QVBoxLayout()

        # Step 1: Patterns
        layout.addWidget(QLabel("<b>1. Search Patterns:</b>"))
        row1 = QHBoxLayout()
        self.pattern_input = QLineEdit(placeholderText="Enter regex or load file...")  # type: ignore
        self.btn_load_txt = QPushButton("📂 Load .txt")
        self.btn_load_txt.clicked.connect(self.select_pattern_file)
        row1.addWidget(self.pattern_input)
        row1.addWidget(self.btn_load_txt)
        layout.addLayout(row1)

        # Step 2: Source
        layout.addWidget(QLabel("<b>2. Source Folder:</b>"))
        row2 = QHBoxLayout()
        self.input_path_display = QLineEdit()
        self.btn_browse_input = QPushButton("📁 Browse Source")
        self.btn_browse_input.clicked.connect(self.select_input_folder)
        row2.addWidget(self.input_path_display)
        row2.addWidget(self.btn_browse_input)
        layout.addLayout(row2)

        # Step 3: Destination
        layout.addWidget(QLabel("<b>3. Output Destination:</b>"))
        row3 = QHBoxLayout()
        self.output_path_input = QLineEdit()
        self.btn_browse_output = QPushButton("📁 Browse Output")
        self.btn_browse_output.clicked.connect(self.select_output_folder)
        row3.addWidget(self.output_path_input)
        row3.addWidget(self.btn_browse_output)
        layout.addLayout(row3)

        # Options
        opts = QHBoxLayout()
        self.is_regex = QCheckBox("Use Regex")
        self.case_sensitive = QCheckBox("Case Sensitive")
        self.recursive = QCheckBox("Recursive")
        self.recursive.setChecked(True)
        opts.addWidget(self.is_regex)
        opts.addWidget(self.case_sensitive)
        opts.addWidget(self.recursive)
        layout.addLayout(opts)

        # Action
        self.btn_run = QPushButton("🚀 START EXTRACTION")
        self.btn_run.clicked.connect(self.start_process)
        layout.addWidget(self.btn_run)

        # Log View
        layout.addWidget(QLabel("<b>Real-time Process Log:</b>"))
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)

        # Log monitoring timer
        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self.update_log_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_pattern_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Pattern File", "", "Text Files (*.txt)"
        )
        if file_path:
            self.active_patterns = load_search_inputs(file_path)
            self.pattern_input.setText(f"Loaded {len(self.active_patterns)} patterns.")
            self.pattern_input.setDisabled(True)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Source")
        if folder:
            self.input_path_display.setText(folder)
            default_out = Path.home() / "Documents" / f"{Path(folder).name}_extracted"
            self.output_path_input.setText(str(default_out))

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination")
        if folder:
            self.output_path_input.setText(folder)

    def start_process(self):
        out_dir = self.output_path_input.text()
        in_dir = self.input_path_display.text()

        if not out_dir or not in_dir:
            return

        # LONG PATH FIX (The Extended-Length Path Prefix)
        abs_out = os.path.abspath(out_dir)
        if sys.platform == "win32" and not abs_out.startswith("\\\\?\\"):
            abs_out = "\\\\?\\" + abs_out

        self.log_file_path = Path(out_dir) / "pdf_extractor.log"
        self.last_log_size = 0
        self.log_box.clear()

        patterns = (
            self.active_patterns
            if self.active_patterns
            else [self.pattern_input.text()]
        )
        cpu_count = os.cpu_count() or 1
        stable_workers = max(1, int(cpu_count * 0.8))

        config = ExtractionConfig(
            pattern_inputs=patterns,
            use_regex=self.is_regex.isChecked(),
            case_sensitive=self.case_sensitive.isChecked(),
            whole_word=False,
            output_dir=str(abs_out),  # Send the long-path aware version
            input_dirs=[in_dir],
            file_patterns=["*.pdf"],
            max_workers=stable_workers,
            log_level="INFO",
            recursive=self.recursive.isChecked(),
            dry_run=False,
        )

        self.btn_run.setEnabled(False)
        self.worker = ExtractionWorker(config)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
        self.log_timer.start(500)

    def update_log_box(self):
        # We check the log file inside the original out_dir (non-prefixed for standard open)
        actual_log = Path(self.output_path_input.text()) / "pdf_extractor.log"
        if actual_log.exists():
            current_size = actual_log.stat().st_size
            if current_size > self.last_log_size:
                with open(actual_log, "r", encoding="utf-8") as f:
                    f.seek(self.last_log_size)
                    self.log_box.append(f.read().strip())
                self.last_log_size = current_size

    def on_finished(self, stats):
        self.log_timer.stop()
        self.update_log_box()
        self.btn_run.setEnabled(True)
        self.status_label.setText("Extraction Complete.")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    window = PDFExtractGUI()
    window.show()
    sys.exit(app.exec())
