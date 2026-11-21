import argparse
import json
import sys
from pathlib import Path

def read_snapshot(path):
    entries = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(entries, dict) or any(
        not isinstance(command, str) for command in entries.values()
    ):
        raise ValueError(f"Invalid snapshot: {path}")
    return entries


def compare_snapshots(before_path, after_path):
    before = read_snapshot(before_path)
    after = read_snapshot(after_path)

    if before == after:
        print("No changes.")
        return

    for location in sorted(before.keys() | after.keys()):
        old = before.get(location)
        new = after.get(location)
        if old is None:
            print(f"ADDED {location!r}: {new!r}")
        elif new is None:
            print(f"REMOVED {location!r}: {old!r}")
        elif old != new:
            print(f"CHANGED {location!r}: {old!r} -> {new!r}")
def main():
    parser = argparse.ArgumentParser(prog="python -m persist_diff")
    commands = parser.add_subparsers(dest="command", required=True)
    snapshot = commands.add_parser("snapshot", help="save a Windows snapshot")
    snapshot.add_argument("output", type=Path)
    diff = commands.add_parser("diff", help="compare two saved snapshots")
    diff.add_argument("before", type=Path)
    diff.add_argument("after", type=Path)
    args = parser.parse_args()

    if args.command == "diff":
        try:
            compare_snapshots(args.before, args.after)
        except (OSError, ValueError) as error:
            parser.exit(1, f"Diff failed: {error}\n")
        return

    if sys.platform != "win32":
        parser.error("Snapshot collection requires Windows.")

    from . import run_keys, scheduled_tasks, winlogon, startup_folders, services

    try:
        entries = run_keys.collect() | scheduled_tasks.collect() | winlogon.collect() | startup_folders.collect() | services.collect()
        with args.output.open("x", encoding="utf-8") as output:
            json.dump(entries, output, indent=2, sort_keys=True)
            output.write("\n")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Snapshot failed: {error}\n")

    print(f"Saved {len(entries)} entries to {args.output}")


if __name__ == "__main__":
    main()
