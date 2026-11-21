"""Collect the Winlogon Shell and Userinit values, which run at logon."""
import winreg

HIVES = {
    "HKLM": winreg.HKEY_LOCAL_MACHINE,
    "HKCU": winreg.HKEY_CURRENT_USER,
}

PATH = r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon"

NAMES = ["Shell", "Userinit"]


def collect():
    results = {}
    for hive_name, hive in HIVES.items():
        try:
            with winreg.OpenKey(hive, PATH) as key:
                for name in NAMES:
                    try:
                        value, _ = winreg.QueryValueEx(key, name)
                    except FileNotFoundError:
                        continue
                    results[f"{hive_name}\\{PATH}\\{name}"] = str(value)
        except FileNotFoundError:
            pass
    return results


if __name__ == "__main__":
    for location, command in collect().items():
        print(location)
        print("    " + command)
