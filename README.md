# LaTeX-Live: A Local Live-Previewer for LaTeX

LaTeX-Live is a command-line tool that brings the convenience of a live-reloading preview, similar to Overleaf, to your local machine. It features a user-friendly, interactive menu system that runs directly in your terminal.

Write your LaTeX in your favorite code editor, and use this tool to handle the compilation and previewing automatically.

## Features

- **Interactive Menu**: A clean, arrow-key navigable menu to select your files and actions. No need to remember command-line arguments.
- **Live-Reload**: Automatically detects changes when you save your `.tex` file and recompiles the PDF.
- **Manual Build**: Option to compile a document once.
- **Clean Log Viewer**: The live-reload mode features a full-screen, non-scrolling log viewer that displays the compilation status.
- **Intuitive Controls**: Use `Esc` or `Ctrl+C` to gracefully exit the live-reload mode and return to the main menu.
- **Organized Structure**: The project is structured to keep your source `.tex` files neatly separated from the compiled output files.

## Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.x**
2.  **A LaTeX Distribution**: You must have a working LaTeX installation on your system, such that the `pdflatex` command is available in your system's PATH.
    -   **macOS**: [MacTeX](https://www.tug.org/mactex/)
    -   **Windows**: [MiKTeX](https://miktex.org/)
    -   **Linux**: TeX Live (e.g., `sudo apt-get install texlive-full`)

## Installation

1.  **Navigate to the project directory**:
    ```bash
    cd /path/to/LaTeX_Editor
    ```

2.  **Install the required Python libraries**:
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  **Place your documents**: Put your `.tex` files inside the `document/` directory.

2.  **Run the application**:
    ```bash
    python3 run.py
    ```

3.  **Use the Menu**:
    -   You will be greeted by a menu listing all the `.tex` files in the `document/` directory. Use the arrow keys to select one.
    -   A second menu will appear. Choose whether you want to `Compile (Build Once)` or `Watch for Changes (Live Preview)`.
    -   If you choose to watch, the tool will enter a full-screen log mode. When you save your `.tex` file, the log will update. Press `Esc` or `Ctrl+C` to exit and return to the main menu.

## Project Structure

```
LaTeX_Editor/
├── document/         # Your .tex source files go here
│   └── main.tex
├── output/           # All compiled files (.pdf, .log, .aux) are stored here
├── src/
│   └── latex_live/   # The application's Python source code
│       ├── __init__.py
│       ├── cli.py          # The interactive menu logic
│       ├── compiler.py     # The pdflatex compilation logic
│       ├── watcher.py      # The file watching and live-reload UI
│       └── utils.py        # Helper functions (e.g., opening the PDF)
├── .gitignore        # Ignores temporary files and output
├── README.md         # This file
├── requirements.txt  # Python dependencies
└── run.py            # The main script to launch the application
```
