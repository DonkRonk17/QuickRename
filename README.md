<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/1a4338b1-ab15-4c3d-a2a5-4494c58d00c3" />

# ⚡ QuickRename

**Batch File Renamer with Live Preview**

A fast, intuitive desktop application for renaming multiple files at once. See your changes before applying them!

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

---

## ✨ Features

- **Live Preview** - See exactly how files will be renamed before applying
- **Drag & Drop** - Simply drag files into the window
- **7 Rename Modes**:
  - 🔍 **Find & Replace** - Replace text (with regex support!)
  - ➕ **Add Prefix/Suffix** - Add text before or after filenames
  - 🔤 **Change Case** - lowercase, UPPERCASE, Title Case, Sentence case
  - 🔢 **Add Sequence** - Add numbers (001, 002, 003...)
  - 📅 **Add Date** - Add current date in various formats
  - ✂️ **Remove Characters** - Strip unwanted characters
  - 📏 **Trim Filename** - Remove characters from start/end
- **Modern Dark UI** - Beautiful, easy on the eyes
- **No Installation** - Just run the Python script
- **Cross-Platform** - Works on Windows, macOS, and Linux

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/DonkRonk17/QuickRename.git
   cd QuickRename
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python quickrename.py
   ```

That's it! The application will open and you're ready to rename files.

---

## 📖 How to Use

### Step 1: Add Files
- **Drag & Drop** files directly into the window, OR
- Click **"Add Files"** button to browse

### Step 2: Choose Rename Mode
Select from the dropdown:
- **Find & Replace** - Enter text to find and replacement text
- **Add Prefix/Suffix** - Enter text to add before/after filename
- **Change Case** - Select case style from dropdown
- **Add Sequence** - Set start number, padding, and position
- **Add Date** - Choose date format and position
- **Remove Characters** - Enter characters to remove
- **Trim Filename** - Set number of characters to trim

### Step 3: Preview Changes
The right panel shows:
- Original filename
- Arrow (→)
- New filename (highlighted in green if changed)

### Step 4: Apply
Click **"✨ Rename Files"** to apply all changes.

---

## 🎨 Rename Modes Explained

### Find & Replace
Replace text in filenames. Supports regular expressions!

| Find | Replace | Example |
|------|---------|---------|
| `IMG_` | `Photo_` | `IMG_001.jpg` → `Photo_001.jpg` |
| `\d+` (regex) | `X` | `file123.txt` → `fileX.txt` |

### Add Prefix/Suffix
Add text before or after the filename (before extension).

| Prefix | Suffix | Example |
|--------|--------|---------|
| `2024_` | `_final` | `report.pdf` → `2024_report_final.pdf` |

### Change Case
Convert filename to different cases.

| Mode | Example |
|------|---------|
| lowercase | `My File.txt` → `my file.txt` |
| UPPERCASE | `My File.txt` → `MY FILE.TXT` |
| Title Case | `my file.txt` → `My File.txt` |
| Sentence case | `MY FILE.txt` → `My file.txt` |

### Add Sequence
Add sequential numbers to files.

| Start | Padding | Position | Example |
|-------|---------|----------|---------|
| 1 | 3 | Prefix | `photo.jpg` → `001_photo.jpg` |
| 100 | 4 | Suffix | `photo.jpg` → `photo_0100.jpg` |
| 1 | 2 | Replace | `photo.jpg` → `01.jpg` |

### Add Date
Add current date to filenames.

| Format | Position | Example |
|--------|----------|---------|
| `%Y-%m-%d` | Prefix | `file.txt` → `2026-01-01_file.txt` |
| `%Y%m%d_%H%M%S` | Suffix | `file.txt` → `file_20260101_143052.txt` |

### Remove Characters
Remove specific characters from filenames.

| Remove | Example |
|--------|---------|
| `_-` | `my_file-name.txt` → `myfilename.txt` |
| `()` | `photo (1).jpg` → `photo 1.jpg` |

### Trim Filename
Remove characters from the start or end of filenames.

| From Start | From End | Example |
|------------|----------|---------|
| 4 | 0 | `IMG_photo.jpg` → `photo.jpg` |
| 0 | 5 | `document_v1.0.pdf` → `document.pdf` |

---

## ⌨️ Tips & Tricks

1. **Regex Power**: In Find & Replace mode, check "Use Regular Expressions" for advanced patterns
2. **Preview First**: Always check the preview before clicking Rename
3. **Batch Processing**: Add hundreds of files at once - no limit!
4. **Undo**: If you make a mistake, use your OS file history or backup

---

## 🛠️ Requirements

```
PySide6>=6.6.0
```

The application uses only PySide6 for the GUI - no other dependencies needed!

---

## 📁 Project Structure

```
QuickRename/
├── quickrename.py      # Main application (single file!)
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── LICENSE            # MIT License
```
<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/8d576970-feac-45ec-a9ab-9b894ed60930" />

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Randell Logan Smith** (Logan)  
[Metaphy LLC](https://github.com/DonkRonk17)

---

## 🙏 Acknowledgments

- Built with [PySide6](https://wiki.qt.io/Qt_for_Python) (Qt for Python)
- Inspired by the need for a simple, free batch renamer
- Part of the Team Brain AI Collaborative project

---

*Made with ⚡ by Team Brain*
