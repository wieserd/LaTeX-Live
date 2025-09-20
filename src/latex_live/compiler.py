import subprocess
import pathlib

def compile_latex(tex_file: pathlib.Path, output_dir: pathlib.Path, engine: str) -> tuple[bool, str]:
    """Compiles a .tex file and returns a success flag and the output log."""
    if not tex_file.exists():
        return False, f"Error: File not found at {tex_file}"

    log = [f"Compiling {tex_file.name} with '{engine}' into {output_dir}..."]
    command = [
        engine,
        f"-output-directory={output_dir.resolve()}",
        "-interaction=nonstopmode",
        str(tex_file.resolve())
    ]

    try:
        log.append("--- Pass 1 ---")
        subprocess.run(command, capture_output=True, text=True, check=True)
        
        log.append("--- Pass 2 ---")
        subprocess.run(command, capture_output=True, text=True, check=True)
        
        log.append("\nCompilation successful.")
        return True, "\n".join(log)

    except FileNotFoundError:
        error_msg = f"Error: '{engine}' command not found. Please ensure it is installed and in your system's PATH."
        log.append(error_msg)
        return False, "\n".join(log)

    except subprocess.CalledProcessError:
        log.append("\nCompilation failed.")
        log_file = output_dir / tex_file.with_suffix('.log').name
        if log_file.exists():
            log.append(f"An error occurred. See the log file for details: {log_file}")
            # Try to find the error in the log file
            try:
                log_content = log_file.read_text().split('!')[1:] # Look for text after the first '!'
                if log_content:
                    log.append("\n--- Potential Error ---")
                    log.append(log_content[0].strip())
                    log.append("-----------------------")
            except Exception:
                log.append("Could not parse log file for a specific error.")
        else:
            log.append("Compilation failed and no log file was produced.")
        return False, "\n".join(log)
