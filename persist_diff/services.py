"""Collect Windows services and the commands they run."""
import winreg

PATH = r"SYSTEM\CurrentControlSet\Services"

START_TYPES = {0: "Boot", 1: "System", 2: "Auto", 3: "Manual", 4: "Disabled"}


def collect():
    results = {}
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, PATH) as key:
        i = 0
        while True:
            try:
                name = winreg.EnumKey(key, i)
            except OSError:
                break
            i += 1
            try:
                with winreg.OpenKey(key, name) as sub:
                    image_path, _ = winreg.QueryValueEx(sub, "ImagePath")
                    start, _ = winreg.QueryValueEx(sub, "Start")
            except OSError:
                continue
            start_name = START_TYPES.get(start, str(start))
            results[f"HKLM\\{PATH}\\{name}"] = f"{image_path} (start: {start_name})"
    return results


if __name__ == "__main__":
    for location, command in collect().items():
        print(location)
        print("    " + command)