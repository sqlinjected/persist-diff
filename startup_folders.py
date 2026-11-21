"""Collect files in the per-user and all-users Startup folders."""
import os
from pathlib import Path

FOLDERS = {
    "User": os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup"),
    "AllUsers": os.path.join(os.environ.get("PROGRAMDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup"),
}


def collect():
    results = {}
    for scope, folder in FOLDERS.items():
        path = Path(folder)
        if not path.is_dir():
            continue
        for item in path.iterdir():
            if item.name.lower() == "desktop.ini":
                continue
            stat = item.stat()
            results[f"Startup\\{scope}\\{item.name}"] = f"{item} ({stat.st_size} bytes, modified {int(stat.st_mtime)})"
    return results


if __name__ == "__main__":
    for location, command in collect().items():
        print(location)
        print("    " + command)
