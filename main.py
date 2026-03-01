"""CLI entrypoint for the Log Analytics Engine.

Usage:
  python main.py --file path/to/logfile [--level INFO] [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD] [--export-json out.json]
"""
import time
import argparse
import json
import logging
import re
from datetime import timedelta
from typing import Optional

from analyzer import LogAnalyzer, parse_date_input


DATE_ONLY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _maybe_expand_date(date_str: Optional[str], is_end: bool = False):
    if date_str is None:
        return None
    dt = parse_date_input(date_str)
    if DATE_ONLY_RE.match(date_str):
        if is_end:
            # make end of day
            return dt + timedelta(hours=23, minutes=59, seconds=59)
        return dt
    return dt


def format_output(stats: dict) -> str:
    lines = []
    lines.append(f"Total Logs: {stats['total']}")
    lines.append(f"INFO: {stats['INFO']}")
    lines.append(f"WARNING: {stats['WARNING']}")
    lines.append(f"ERROR: {stats['ERROR']}")
    lines.append(f"Most Frequent IP: {stats['most_ip']}")
    lines.append("Top 3 Errors:")
    for i, (msg, count) in enumerate(stats['top3_errors'], start=1):
        lines.append(f"{i}. {msg} ({count})")
        
    
    lines.append(f"First Log Time: {stats['first_log_time']}")
    lines.append(f"Last Log Time: {stats['last_log_time']}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Log Analytics Engine")
    parser.add_argument("--file", required=True, help="Path to log file")
    parser.add_argument("--level", choices=["INFO", "WARNING", "ERROR"], help="Filter by level")
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--end-date", help="End date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--export-json", help="Export statistics to JSON file")

    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    start_dt = _maybe_expand_date(args.start_date, is_end=False)
    end_dt = _maybe_expand_date(args.end_date, is_end=True)

    analyzer = LogAnalyzer(level_filter=args.level, start_date=start_dt, end_date=end_dt)
    start = time.perf_counter()

    analyzer.process_file(args.file)
    stats = analyzer.get_stats()

    end = time.perf_counter()
    output = format_output(stats)
    print(output)
    print(f"\nProcessed in {end - start:.4f} seconds")

    if args.export_json:
        try:
            with open(args.export_json, "w", encoding="utf-8") as outfh:
                json.dump(stats, outfh, ensure_ascii=False, indent=2)
        except Exception as exc:
            logging.getLogger(__name__).warning("Failed to export JSON: %s", exc)


if __name__ == "__main__":
    main()
