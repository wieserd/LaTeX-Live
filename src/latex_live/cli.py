import questionary
import pathlib
import sys
import argparse
import shutil

from .watcher import watch_file, build_and_open

def create_new_project(project_name: str, template: str):
    """Creates a new, self-contained LaTeX-Live project in a new directory."""
    print(f"Creating new project '{project_name}'...")
    project_dir = pathlib.Path(project_name)
    if project_dir.exists():
        print(f"Error: Directory '{project_name}' already exists.")
        sys.exit(1)

    # --- Create project structure ---
    document_dir = project_dir / "document"
    output_dir = project_dir / "output"
    document_dir.mkdir(parents=True)
    output_dir.mkdir()

    # --- Copy application source to make the project self-contained ---
    # This assumes the script is run from the root of the LaTeX_Editor project
    app_src_dir = pathlib.Path("src")
    app_run_script = pathlib.Path("run.py")
    app_reqs_file = pathlib.Path("requirements.txt")

    shutil.copytree(app_src_dir, project_dir / "src")
    shutil.copy(app_run_script, project_dir)
    shutil.copy(app_reqs_file, project_dir)

    # --- Copy template ---
    template_dir = app_src_dir / "latex_live" / "templates"
    template_file = template_dir / f"{template}.tex"
    if not template_file.exists():
        print(f"Warning: Template '{template}' not found. Using default article template.")
        template_file = template_dir / "article.tex"

    shutil.copy(template_file, document_dir / "main.tex")

    # --- Create default config file ---
    default_config = "[compiler]\nengine = pdflatex\n"
    (project_dir / "project.cfg").write_text(default_config)

    print("\nProject created successfully!")
    print("\nNext steps:")
    print(f"  1. cd {project_name}")
    print(f"  2. pip install -r requirements.txt")
    print(f"  3. python3 run.py")

import configparser
from questionary import Separator

def change_compiler_engine(config: configparser.ConfigParser):
    """Displays a menu to change the compiler engine and saves the choice."""
    new_engine = questionary.select(
        "Select a new compiler engine:",
        choices=["pdflatex", "lualatex", "xelatex"],
        default=config.get('compiler', 'engine', fallback='pdflatex')
    ).ask()

    if new_engine:
        config.set('compiler', 'engine', new_engine)
        with open('project.cfg', 'w') as configfile:
            config.write(configfile)
        print(f"\nCompiler engine set to '{new_engine}'. It will be used on the next compilation.")
        questionary.press_any_key_to_continue("Press any key to return to the menu...").ask()

def run_interactive_menu():
    """The main entry point for the interactive CLI."""
    config = configparser.ConfigParser()

    document_dir = pathlib.Path("document")
    output_dir = pathlib.Path("output")

    if not document_dir.exists():
        print(f"Error: The 'document' directory was not found.")
        print("Are you inside a LaTeX-Live project? If not, create one with:")
        print("python3 run.py --new <your_project_name>")
        sys.exit(1)

    output_dir.mkdir(exist_ok=True)

    try:
        while True:
            # Read configuration at the start of each loop to reflect changes
            config.read('project.cfg')
            engine = config.get('compiler', 'engine', fallback='pdflatex')

            tex_files = sorted(list(document_dir.glob("*.tex")))
            if not tex_files:
                print(f"Error: No .tex files found in the '{document_dir}' directory.")
                sys.exit(1)

            choices = [f.name for f in tex_files] + [
                Separator(),
                "Change Compiler Engine",
                "Exit"
            ]

            selected_choice = questionary.select(
                f"Welcome to LaTeX-Live! (Engine: {engine}) Which document do you want to work on?",
                choices=choices
            ).ask()

            if selected_choice is None or selected_choice == "Exit":
                print("Goodbye!")
                break

            if selected_choice == "Change Compiler Engine":
                change_compiler_engine(config)
                continue
            
            selected_file = document_dir / selected_choice

            action = questionary.select(
                f"What do you want to do with '{selected_file.name}'?",
                choices=["Compile (Build Once)", "Watch for Changes (Live Preview)", "Back to file selection"]
            ).ask()

            if action is None or action == "Back to file selection":
                continue

            if action == "Compile (Build Once)":
                log = build_and_open(selected_file, output_dir, engine)
                print(log)
                questionary.press_any_key_to_continue("Build complete. Press any key to return...").ask()
            
            elif action == "Watch for Changes (Live Preview)":
                watch_file(selected_file, output_dir, engine)

    except KeyboardInterrupt:
        print("\nGoodbye!")

def main():
    parser = argparse.ArgumentParser(description="A local live-previewer for LaTeX.")
    parser.add_argument("--new", dest="project_name", help="Create a new, self-contained project.")
    parser.add_argument("--template", default="article", choices=["article", "report"], help="Specify a template for the new project.")
    args = parser.parse_args()

    if args.project_name:
        create_new_project(args.project_name, args.template)
    else:
        run_interactive_menu()
