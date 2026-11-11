"""Collect autostart entries from the registry Run and RunOnce keys."""
import winreg

HIVES = {
    "HKLM": winreg.HKEY_LOCAL_MACHINE,
    "HKCU": winreg.HKEY_CURRENT_USER,
}

PATHS = [
    r"Software\Microsoft\Windows\CurrentVersion\Run",
    r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
    r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run",
    r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\RunOnce",
]


def read_key(hive, path):
    entries = {}
    try:
        with winreg.OpenKey(hive, path) as key:
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                except OSError:
                    break
                entries[name] = str(value)
                i += 1
    except FileNotFoundError:
        pass
    return entries


def collect():
    results = {}
    for hive_name, hive in HIVES.items():
        for path in PATHS:
            for name, command in read_key(hive, path).items():
                results[f"{hive_name}\\{path}\\{name}"] = command
    return results


if __name__ == "__main__":
    for location, command in collect().items():
        print(location)
        print("    " + command)