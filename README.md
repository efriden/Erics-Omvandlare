# Erics-Omvandlare

A Python conversion utility application.

## Description

This project provides conversion utilities for various formats and units.

## Setup

### Prerequisites
- Python 3.11 or higher

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd Erics-Omvandlare
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   py -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface
To run the command line application:
```bash
python src/main.py
```

### Graphical User Interface (GUI)
To start the GUI application:
```bash
# Option 1: Direct launch
python src/gui.py

# Option 2: Using launcher script
python run_gui.py

# Option 3: Windows batch file (double-click)
run_gui.bat
```

### GUI Features
- **Text Input**: Large text area for pasting or typing Markdown content
- **Export to PDF**: Convert your text to PDF format
- **Export to DOCX**: Convert your text to Microsoft Word format
- **Clear Text**: Clear the text area with one click
- **Status Bar**: Shows current operation status
- **Auto-filename**: Generates timestamped filenames automatically

## Development

### Project Structure
```
Erics-Omvandlare/
├── src/                 # Source code
├── tests/               # Test files
├── docs/                # Documentation
├── venv/                # Virtual environment
├── requirements.txt     # Project dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### Running Tests
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
