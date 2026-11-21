# persist-diff

Snapshot the places Windows uses to auto-start programs, then diff two snapshots to see what changed.

Useful for checking what an installer, update, or sketchy download added to your system.

## What it checks

- Run and RunOnce keys (HKLM + HKCU, including 32-bit WOW6432Node)
- Scheduled tasks
- Winlogon Shell and Userinit

Planned: services, startup folders.

## Requirements

- Windows (for taking snapshots)
- Python 3

## Usage

Take a snapshot before you install something:

```
python -m persist_diff snapshot before.json
```

Install / run whatever you're testing, then take another one:

```
python -m persist_diff snapshot after.json
```

Compare them:

```
python -m persist_diff diff before.json after.json
```

If nothing changed you'll get `No changes.` Otherwise you get one line per location marked `ADDED`, `REMOVED`, or `CHANGED`.

Snapshots won't overwrite an existing file, so use a new name each time.

## Notes

- Run as admin if you want to see everything. Some scheduled tasks are hidden from normal users.
- It only reads. It doesn't change or delete anything on your system.

## License

MIT
