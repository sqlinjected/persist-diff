"""Collect scheduled tasks and the commands they run."""
import os
import xml.etree.ElementTree as ET

TASKS_DIR = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "Tasks")
NS = {"t": "http://schemas.microsoft.com/windows/2004/02/mit/task"}


def read_task(path):
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, PermissionError, OSError):
        return None
    commands = []
    for ex in root.findall("t:Actions/t:Exec", NS):
        cmd = ex.findtext("t:Command", default="", namespaces=NS)
        args = ex.findtext("t:Arguments", default="", namespaces=NS)
        commands.append(f"{cmd} {args}".strip())
    return " | ".join(commands) if commands else "(no command)"


def collect():
    results = {}
    for folder, _, files in os.walk(TASKS_DIR):
        for name in files:
            full = os.path.join(folder, name)
            command = read_task(full)
            if command is not None:
                task = os.path.relpath(full, TASKS_DIR)
                results[f"Task\\{task}"] = command
    return results


if __name__ == "__main__":
    for location, command in collect().items():
        print(location)
        print("    " + command)