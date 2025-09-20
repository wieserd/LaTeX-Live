import subprocess
import pathlib
import sys

def open_pdf(pdf_file: pathlib.Path):
    """Opens a PDF file using the system's default viewer."""
    if not pdf_file.exists():
        print(f"Error: PDF file not found at {pdf_file}")
        return
    
    print(f"Opening {pdf_file.name}...")
    try:
        if sys.platform == "darwin": # macOS
            subprocess.run(["open", pdf_file], check=True)
        elif sys.platform == "win32": # Windows
            subprocess.run(["start", pdf_file], check=True, shell=True)
        else: # linux
            subprocess.run(["xdg-open", pdf_file], check=True)
    except FileNotFoundError:
        print(f"Error: Could not open PDF. Please open it manually.")
    except subprocess.CalledProcessError:
        print(f"Error: Failed to open PDF viewer.")
