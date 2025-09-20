import time
import pathlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .compiler import compile_latex
from .utils import open_pdf

# prompt_toolkit imports
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import VSplit, Window, HSplit
from prompt_toolkit.widgets import Frame, TextArea


def build_and_open(tex_file: pathlib.Path, output_dir: pathlib.Path, engine: str):
    """Compiles the .tex file, opens the PDF, and returns the log."""
    success, log = compile_latex(tex_file, output_dir, engine)
    if success:
        pdf_file = output_dir / tex_file.with_suffix(".pdf").name
        open_pdf(pdf_file)
    return log

class LaTeXChangeHandler(FileSystemEventHandler):
    """Reacts to changes in the .tex file and updates the UI."""
    def __init__(self, tex_file: pathlib.Path, output_dir: pathlib.Path, app: Application, engine: str):
        self.tex_file = tex_file
        self.output_dir = output_dir
        self.app = app
        self.engine = engine
        self.last_run = 0

    def on_modified(self, event):
        if time.time() - self.last_run < 1:
            return

        if not event.is_directory and pathlib.Path(event.src_path).resolve() == self.tex_file.resolve():
            self.app.loop.call_soon_threadsafe(self.recompile)
            self.last_run = time.time()

    def recompile(self):
        """The actual recompilation logic."""
        log_text = build_and_open(self.tex_file, self.output_dir, self.engine)
        
        text_area = self.app.layout.get_children()[0].content
        text_area.document = Document(log_text, cursor_position=len(log_text))


def watch_file(tex_file: pathlib.Path, output_dir: pathlib.Path, engine: str):
    """Watches a .tex file and recompiles on change using a prompt_toolkit UI."""
    initial_log = build_and_open(tex_file, output_dir, engine)

    log_area = TextArea(text=initial_log, read_only=True, scrollbar=True, wrap_lines=False)
    status_bar = Window(
        content=FormattedTextControl(text=f"Engine: {engine} | Press Esc or Ctrl+C to exit."),
        height=1,
        style="class:status-bar"
    )

    root_container = HSplit([
        Frame(body=log_area, title=f"Watching {tex_file.name}"),
        status_bar
    ])

    layout = Layout(root_container)

    kb = KeyBindings()
    @kb.add("escape")
    @kb.add("c-c")
    def _(event):
        event.app.exit()

    app = Application(layout=layout, key_bindings=kb, full_screen=True)

    event_handler = LaTeXChangeHandler(tex_file, output_dir, app, engine)
    observer = Observer()
    observer.schedule(event_handler, tex_file.parent, recursive=False)
    observer.start()

    app.run()

    observer.stop()
    observer.join()
