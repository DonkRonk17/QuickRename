#!/usr/bin/env python3
"""
QuickRename - Batch File Renamer with Live Preview
A fast, intuitive tool for renaming multiple files at once.

Author: Randell Logan Smith (Logan) / Metaphy LLC
License: MIT
Version: 1.0.0
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QFileDialog, QComboBox, QSpinBox, QCheckBox, QGroupBox,
    QMessageBox, QHeaderView, QFrame, QSplitter, QStatusBar
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QFont, QColor


# ═══════════════════════════════════════════════════════════════════════════════
# THEME - Modern Dark with Amber Accents
# ═══════════════════════════════════════════════════════════════════════════════

STYLESHEET = """
QMainWindow {
    background-color: #1a1a2e;
}

QWidget {
    background-color: #1a1a2e;
    color: #eaeaea;
    font-family: 'Segoe UI', 'SF Pro Display', sans-serif;
    font-size: 13px;
}

QGroupBox {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
    color: #f39c12;
}

QPushButton {
    background-color: #0f3460;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    color: #eaeaea;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1a4a7a;
}

QPushButton:pressed {
    background-color: #0a2540;
}

QPushButton#primaryBtn {
    background-color: #f39c12;
    color: #1a1a2e;
}

QPushButton#primaryBtn:hover {
    background-color: #f5ab35;
}

QPushButton#dangerBtn {
    background-color: #c0392b;
}

QPushButton#dangerBtn:hover {
    background-color: #e74c3c;
}

QLineEdit {
    background-color: #16213e;
    border: 2px solid #0f3460;
    border-radius: 6px;
    padding: 8px 12px;
    color: #eaeaea;
}

QLineEdit:focus {
    border-color: #f39c12;
}

QComboBox {
    background-color: #16213e;
    border: 2px solid #0f3460;
    border-radius: 6px;
    padding: 8px 12px;
    min-width: 150px;
}

QComboBox:focus {
    border-color: #f39c12;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #f39c12;
    margin-right: 10px;
}

QSpinBox {
    background-color: #16213e;
    border: 2px solid #0f3460;
    border-radius: 6px;
    padding: 8px;
}

QSpinBox:focus {
    border-color: #f39c12;
}

QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid #0f3460;
    background-color: #16213e;
}

QCheckBox::indicator:checked {
    background-color: #f39c12;
    border-color: #f39c12;
}

QTableWidget {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 8px;
    gridline-color: #0f3460;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #0f3460;
}

QTableWidget::item:selected {
    background-color: #0f3460;
}

QHeaderView::section {
    background-color: #0f3460;
    color: #f39c12;
    padding: 10px;
    border: none;
    font-weight: bold;
}

QStatusBar {
    background-color: #0f3460;
    color: #eaeaea;
}

QLabel#dropLabel {
    background-color: #16213e;
    border: 3px dashed #0f3460;
    border-radius: 12px;
    padding: 40px;
    font-size: 16px;
    color: #7f8c8d;
}

QLabel#dropLabel:hover {
    border-color: #f39c12;
    color: #f39c12;
}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# RENAMING ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class RenameEngine:
    """Handles all file renaming logic with preview capability."""
    
    @staticmethod
    def find_replace(filename: str, find: str, replace: str, use_regex: bool = False) -> str:
        """Find and replace text in filename."""
        if not find:
            return filename
        
        name, ext = os.path.splitext(filename)
        
        if use_regex:
            try:
                name = re.sub(find, replace, name)
            except re.error:
                return filename
        else:
            name = name.replace(find, replace)
        
        return name + ext
    
    @staticmethod
    def add_prefix(filename: str, prefix: str) -> str:
        """Add prefix to filename."""
        if not prefix:
            return filename
        return prefix + filename
    
    @staticmethod
    def add_suffix(filename: str, suffix: str) -> str:
        """Add suffix before extension."""
        if not suffix:
            return filename
        name, ext = os.path.splitext(filename)
        return name + suffix + ext
    
    @staticmethod
    def change_case(filename: str, case_type: str) -> str:
        """Change filename case."""
        name, ext = os.path.splitext(filename)
        
        if case_type == "lowercase":
            name = name.lower()
        elif case_type == "UPPERCASE":
            name = name.upper()
        elif case_type == "Title Case":
            name = name.title()
        elif case_type == "Sentence case":
            name = name.capitalize()
        
        return name + ext
    
    @staticmethod
    def add_sequence(filename: str, index: int, start: int, padding: int, position: str) -> str:
        """Add sequential number to filename."""
        number = str(start + index).zfill(padding)
        name, ext = os.path.splitext(filename)
        
        if position == "Prefix":
            return f"{number}_{name}{ext}"
        elif position == "Suffix":
            return f"{name}_{number}{ext}"
        else:  # Replace
            return f"{number}{ext}"
    
    @staticmethod
    def add_date(filename: str, date_format: str, position: str) -> str:
        """Add current date to filename."""
        date_str = datetime.now().strftime(date_format)
        name, ext = os.path.splitext(filename)
        
        if position == "Prefix":
            return f"{date_str}_{name}{ext}"
        else:  # Suffix
            return f"{name}_{date_str}{ext}"
    
    @staticmethod
    def remove_chars(filename: str, chars: str) -> str:
        """Remove specific characters from filename."""
        if not chars:
            return filename
        name, ext = os.path.splitext(filename)
        for char in chars:
            name = name.replace(char, "")
        return name + ext
    
    @staticmethod
    def trim_filename(filename: str, trim_start: int, trim_end: int) -> str:
        """Trim characters from start/end of filename."""
        name, ext = os.path.splitext(filename)
        
        if trim_start > 0:
            name = name[trim_start:]
        if trim_end > 0:
            name = name[:-trim_end] if trim_end < len(name) else ""
        
        return name + ext if name else filename


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

class DropZone(QLabel):
    """Drag-and-drop zone for files."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dropLabel")
        self.setText("📁 Drag & Drop Files Here\nor click 'Add Files' button")
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(120)
        self.setAcceptDrops(True)
        self.main_window = parent
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("border-color: #f39c12; color: #f39c12;")
    
    def dragLeaveEvent(self, event):
        self.setStyleSheet("")
    
    def dropEvent(self, event: QDropEvent):
        self.setStyleSheet("")
        files = [url.toLocalFile() for url in event.mimeData().urls() if os.path.isfile(url.toLocalFile())]
        if files and self.main_window:
            self.main_window.add_files(files)


class QuickRenameApp(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.files: List[Path] = []
        self.engine = RenameEngine()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("QuickRename - Batch File Renamer")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(STYLESHEET)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("⚡ QuickRename")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #f39c12;")
        layout.addWidget(title)
        
        subtitle = QLabel("Batch rename files with live preview")
        subtitle.setStyleSheet("font-size: 14px; color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(subtitle)
        
        # Main splitter
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter, 1)
        
        # Left panel - Options
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 10, 0)
        
        # Drop zone
        self.drop_zone = DropZone(self)
        left_layout.addWidget(self.drop_zone)
        
        # File buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("📁 Add Files")
        self.add_btn.clicked.connect(self.browse_files)
        self.clear_btn = QPushButton("🗑️ Clear All")
        self.clear_btn.setObjectName("dangerBtn")
        self.clear_btn.clicked.connect(self.clear_files)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.clear_btn)
        left_layout.addLayout(btn_layout)
        
        # Rename options
        options_group = QGroupBox("Rename Options")
        options_layout = QVBoxLayout(options_group)
        
        # Mode selector
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Mode:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Find & Replace",
            "Add Prefix/Suffix",
            "Change Case",
            "Add Sequence",
            "Add Date",
            "Remove Characters",
            "Trim Filename"
        ])
        self.mode_combo.currentTextChanged.connect(self.on_mode_change)
        mode_layout.addWidget(self.mode_combo, 1)
        options_layout.addLayout(mode_layout)
        
        # Options container (changes based on mode)
        self.options_container = QWidget()
        self.options_container_layout = QVBoxLayout(self.options_container)
        self.options_container_layout.setContentsMargins(0, 10, 0, 0)
        options_layout.addWidget(self.options_container)
        
        left_layout.addWidget(options_group)
        
        # Initialize mode options
        self.create_find_replace_options()
        
        left_layout.addStretch()
        
        # Rename button
        self.rename_btn = QPushButton("✨ Rename Files")
        self.rename_btn.setObjectName("primaryBtn")
        self.rename_btn.setMinimumHeight(50)
        self.rename_btn.setStyleSheet(self.rename_btn.styleSheet() + "font-size: 16px;")
        self.rename_btn.clicked.connect(self.execute_rename)
        left_layout.addWidget(self.rename_btn)
        
        splitter.addWidget(left_panel)
        
        # Right panel - Preview table
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 0, 0, 0)
        
        preview_label = QLabel("📋 Preview")
        preview_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #f39c12;")
        right_layout.addWidget(preview_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Original Name", "→", "New Name"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setColumnWidth(1, 40)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        right_layout.addWidget(self.table)
        
        splitter.addWidget(right_panel)
        splitter.setSizes([350, 650])
        
        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready - Add files to begin")
    
    def clear_options_container(self):
        """Clear all widgets from options container."""
        while self.options_container_layout.count():
            item = self.options_container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def create_find_replace_options(self):
        """Create Find & Replace mode options."""
        self.clear_options_container()
        
        # Find
        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Text to find...")
        self.find_input.textChanged.connect(self.update_preview)
        find_layout.addWidget(self.find_input, 1)
        self.options_container_layout.addLayout(find_layout)
        
        # Replace
        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("Replace:"))
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Replace with...")
        self.replace_input.textChanged.connect(self.update_preview)
        replace_layout.addWidget(self.replace_input, 1)
        self.options_container_layout.addLayout(replace_layout)
        
        # Regex option
        self.regex_check = QCheckBox("Use Regular Expressions")
        self.regex_check.stateChanged.connect(self.update_preview)
        self.options_container_layout.addWidget(self.regex_check)
    
    def create_prefix_suffix_options(self):
        """Create Prefix/Suffix mode options."""
        self.clear_options_container()
        
        # Prefix
        prefix_layout = QHBoxLayout()
        prefix_layout.addWidget(QLabel("Prefix:"))
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("Add before filename...")
        self.prefix_input.textChanged.connect(self.update_preview)
        prefix_layout.addWidget(self.prefix_input, 1)
        self.options_container_layout.addLayout(prefix_layout)
        
        # Suffix
        suffix_layout = QHBoxLayout()
        suffix_layout.addWidget(QLabel("Suffix:"))
        self.suffix_input = QLineEdit()
        self.suffix_input.setPlaceholderText("Add after filename...")
        self.suffix_input.textChanged.connect(self.update_preview)
        suffix_layout.addWidget(self.suffix_input, 1)
        self.options_container_layout.addLayout(suffix_layout)
    
    def create_case_options(self):
        """Create Change Case mode options."""
        self.clear_options_container()
        
        case_layout = QHBoxLayout()
        case_layout.addWidget(QLabel("Convert to:"))
        self.case_combo = QComboBox()
        self.case_combo.addItems(["lowercase", "UPPERCASE", "Title Case", "Sentence case"])
        self.case_combo.currentTextChanged.connect(self.update_preview)
        case_layout.addWidget(self.case_combo, 1)
        self.options_container_layout.addLayout(case_layout)
    
    def create_sequence_options(self):
        """Create Add Sequence mode options."""
        self.clear_options_container()
        
        # Start number
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Start at:"))
        self.seq_start = QSpinBox()
        self.seq_start.setRange(0, 99999)
        self.seq_start.setValue(1)
        self.seq_start.valueChanged.connect(self.update_preview)
        start_layout.addWidget(self.seq_start, 1)
        self.options_container_layout.addLayout(start_layout)
        
        # Padding
        pad_layout = QHBoxLayout()
        pad_layout.addWidget(QLabel("Padding:"))
        self.seq_padding = QSpinBox()
        self.seq_padding.setRange(1, 10)
        self.seq_padding.setValue(3)
        self.seq_padding.valueChanged.connect(self.update_preview)
        pad_layout.addWidget(self.seq_padding, 1)
        self.options_container_layout.addLayout(pad_layout)
        
        # Position
        pos_layout = QHBoxLayout()
        pos_layout.addWidget(QLabel("Position:"))
        self.seq_position = QComboBox()
        self.seq_position.addItems(["Prefix", "Suffix", "Replace Name"])
        self.seq_position.currentTextChanged.connect(self.update_preview)
        pos_layout.addWidget(self.seq_position, 1)
        self.options_container_layout.addLayout(pos_layout)
    
    def create_date_options(self):
        """Create Add Date mode options."""
        self.clear_options_container()
        
        # Format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        self.date_format = QComboBox()
        self.date_format.addItems([
            "%Y-%m-%d",
            "%Y%m%d",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%Y-%m-%d_%H-%M-%S",
            "%Y%m%d_%H%M%S"
        ])
        self.date_format.currentTextChanged.connect(self.update_preview)
        format_layout.addWidget(self.date_format, 1)
        self.options_container_layout.addLayout(format_layout)
        
        # Position
        pos_layout = QHBoxLayout()
        pos_layout.addWidget(QLabel("Position:"))
        self.date_position = QComboBox()
        self.date_position.addItems(["Prefix", "Suffix"])
        self.date_position.currentTextChanged.connect(self.update_preview)
        pos_layout.addWidget(self.date_position, 1)
        self.options_container_layout.addLayout(pos_layout)
    
    def create_remove_options(self):
        """Create Remove Characters mode options."""
        self.clear_options_container()
        
        chars_layout = QHBoxLayout()
        chars_layout.addWidget(QLabel("Remove:"))
        self.remove_chars_input = QLineEdit()
        self.remove_chars_input.setPlaceholderText("Characters to remove (e.g., _-#)")
        self.remove_chars_input.textChanged.connect(self.update_preview)
        chars_layout.addWidget(self.remove_chars_input, 1)
        self.options_container_layout.addLayout(chars_layout)
    
    def create_trim_options(self):
        """Create Trim Filename mode options."""
        self.clear_options_container()
        
        # Trim start
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("From start:"))
        self.trim_start = QSpinBox()
        self.trim_start.setRange(0, 100)
        self.trim_start.valueChanged.connect(self.update_preview)
        start_layout.addWidget(self.trim_start, 1)
        self.options_container_layout.addLayout(start_layout)
        
        # Trim end
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("From end:"))
        self.trim_end = QSpinBox()
        self.trim_end.setRange(0, 100)
        self.trim_end.valueChanged.connect(self.update_preview)
        end_layout.addWidget(self.trim_end, 1)
        self.options_container_layout.addLayout(end_layout)
    
    def on_mode_change(self, mode: str):
        """Handle mode selection change."""
        if mode == "Find & Replace":
            self.create_find_replace_options()
        elif mode == "Add Prefix/Suffix":
            self.create_prefix_suffix_options()
        elif mode == "Change Case":
            self.create_case_options()
        elif mode == "Add Sequence":
            self.create_sequence_options()
        elif mode == "Add Date":
            self.create_date_options()
        elif mode == "Remove Characters":
            self.create_remove_options()
        elif mode == "Trim Filename":
            self.create_trim_options()
        
        self.update_preview()
    
    def browse_files(self):
        """Open file browser dialog."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files to Rename",
            "",
            "All Files (*.*)"
        )
        if files:
            self.add_files(files)
    
    def add_files(self, files: List[str]):
        """Add files to the list."""
        for f in files:
            path = Path(f)
            if path not in self.files:
                self.files.append(path)
        
        self.update_preview()
        self.status.showMessage(f"{len(self.files)} files loaded")
    
    def clear_files(self):
        """Clear all files."""
        self.files.clear()
        self.table.setRowCount(0)
        self.status.showMessage("All files cleared")
    
    def get_new_name(self, filename: str, index: int) -> str:
        """Get the new filename based on current settings."""
        mode = self.mode_combo.currentText()
        
        if mode == "Find & Replace":
            return self.engine.find_replace(
                filename,
                self.find_input.text(),
                self.replace_input.text(),
                self.regex_check.isChecked()
            )
        elif mode == "Add Prefix/Suffix":
            result = self.engine.add_prefix(filename, self.prefix_input.text())
            return self.engine.add_suffix(result, self.suffix_input.text())
        elif mode == "Change Case":
            return self.engine.change_case(filename, self.case_combo.currentText())
        elif mode == "Add Sequence":
            return self.engine.add_sequence(
                filename,
                index,
                self.seq_start.value(),
                self.seq_padding.value(),
                self.seq_position.currentText()
            )
        elif mode == "Add Date":
            return self.engine.add_date(
                filename,
                self.date_format.currentText(),
                self.date_position.currentText()
            )
        elif mode == "Remove Characters":
            return self.engine.remove_chars(filename, self.remove_chars_input.text())
        elif mode == "Trim Filename":
            return self.engine.trim_filename(
                filename,
                self.trim_start.value(),
                self.trim_end.value()
            )
        
        return filename
    
    def update_preview(self):
        """Update the preview table."""
        self.table.setRowCount(len(self.files))
        
        changes = 0
        for i, path in enumerate(self.files):
            original = path.name
            new_name = self.get_new_name(original, i)
            
            # Original name
            orig_item = QTableWidgetItem(original)
            orig_item.setFlags(orig_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(i, 0, orig_item)
            
            # Arrow
            arrow_item = QTableWidgetItem("→")
            arrow_item.setTextAlignment(Qt.AlignCenter)
            arrow_item.setFlags(arrow_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(i, 1, arrow_item)
            
            # New name
            new_item = QTableWidgetItem(new_name)
            new_item.setFlags(new_item.flags() & ~Qt.ItemIsEditable)
            
            # Highlight changes
            if original != new_name:
                new_item.setForeground(QColor("#2ecc71"))
                changes += 1
            
            self.table.setItem(i, 2, new_item)
        
        self.status.showMessage(f"{len(self.files)} files | {changes} will be renamed")
    
    def execute_rename(self):
        """Execute the rename operation."""
        if not self.files:
            QMessageBox.warning(self, "No Files", "Please add files to rename.")
            return
        
        # Collect rename operations
        operations: List[Tuple[Path, Path]] = []
        conflicts = []
        
        for i, path in enumerate(self.files):
            new_name = self.get_new_name(path.name, i)
            new_path = path.parent / new_name
            
            if path.name != new_name:
                if new_path.exists() and new_path != path:
                    conflicts.append(new_name)
                else:
                    operations.append((path, new_path))
        
        if conflicts:
            QMessageBox.warning(
                self,
                "Conflicts Detected",
                f"The following files already exist:\n\n" + "\n".join(conflicts[:10])
            )
            return
        
        if not operations:
            QMessageBox.information(self, "No Changes", "No files need to be renamed.")
            return
        
        # Confirm
        reply = QMessageBox.question(
            self,
            "Confirm Rename",
            f"Rename {len(operations)} file(s)?\n\nThis cannot be undone!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = 0
            errors = []
            
            for old_path, new_path in operations:
                try:
                    old_path.rename(new_path)
                    success += 1
                except Exception as e:
                    errors.append(f"{old_path.name}: {str(e)}")
            
            # Update file list with new paths
            self.files = [
                new_path if (old_path, new_path) in operations else old_path
                for old_path in self.files
                for new_path in [self.files[self.files.index(old_path)].parent / self.get_new_name(old_path.name, self.files.index(old_path))]
            ]
            
            # Refresh
            self.files.clear()
            
            if errors:
                QMessageBox.warning(
                    self,
                    "Some Errors Occurred",
                    f"Renamed {success} files.\n\nErrors:\n" + "\n".join(errors[:5])
                )
            else:
                QMessageBox.information(
                    self,
                    "Success!",
                    f"Successfully renamed {success} file(s)!"
                )
            
            self.table.setRowCount(0)
            self.status.showMessage(f"Renamed {success} files")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = QuickRenameApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
