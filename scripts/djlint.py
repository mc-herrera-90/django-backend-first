from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent


def get_templates():
    """Obtiene todos los templates Django del proyecto."""
    templates = []

    for directory in ROOT.rglob("templates"):
        if not directory.is_dir():
            continue

        if any(part in {".venv", "venv", "node_modules"} for part in directory.parts):
            continue

        templates.extend(directory.rglob("*.html"))

    return sorted(set(templates))


def run_djlint(templates, reformat=False):
    """Ejecuta DjLint sobre los templates encontrados."""
    command = ["djlint"]

    if reformat:
        command.append("--reformat")
    else:
        command.append("--check")

    command.extend(str(template) for template in templates)

    return subprocess.run(command, cwd=ROOT).returncode


def main():
    templates = get_templates()

    if not templates:
        print("No se encontraron templates Django.")
        return 0

    action = "Formateando" if "--format" in sys.argv else "Comprobando"

    print(f"{action} {len(templates)} templates...")

    return run_djlint(
        templates,
        reformat="--format" in sys.argv,
    )


if __name__ == "__main__":
    sys.exit(main())