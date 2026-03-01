# Log Analytics Engine (Python)

Streaming, memory-efficient log analytics tool.

Usage examples:

Run analysis and print to stdout:

```bash
python main.py --file path/to/logfile.log
```

Filter by level and date range, export JSON:

```bash
python main.py --file path/to/logfile.log --level ERROR --start-date 2026-01-01 --end-date 2026-02-01 --export-json out.json
```

Notes:

- Streams files (no full file load).
- Accepts `YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS` for dates.
- Malformed lines are skipped and logged as warnings.
