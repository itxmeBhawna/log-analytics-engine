"""Log analysis core functionality.

Provides the LogAnalyzer class which streams a log file, applies optional
filters, and computes statistics required by the CLI.
"""
from collections import Counter
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any
import logging


class LogAnalyzer:
    """Analyze logs from a file in a streaming fashion.

    Supports filtering by level and date range. Tracks counts, most
    frequent IPs, top error messages, and first/last timestamps.
    """

    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(
        self,
        level_filter: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> None:
        self.level_filter = level_filter
        self.start_date = start_date
        self.end_date = end_date

        self.total_logs: int = 0
        self.level_counts: Counter = Counter()
        self.ip_counts: Counter = Counter()
        self.error_messages: Counter = Counter()

        self.first_log_time: Optional[datetime] = None
        self.last_log_time: Optional[datetime] = None

        self._logger = logging.getLogger(__name__)

    def _parse_line(self, line: str) -> Optional[Tuple[datetime, str, str, str]]:
        """Parse a single log line.

        Expected format:
        YYYY-MM-DD HH:MM:SS LEVEL IP MESSAGE

        Returns (timestamp, level, ip, message) or None if malformed.
        """
        if not line.strip():
            return None

        # Expect first two tokens to be date and time, then level, ip, message
        parts = line.rstrip("\n").split(" ", 4)
        if len(parts) < 5:
            self._logger.warning("Malformed line (too few parts): %s", line.strip())
            return None

        date_part, time_part, level, ip, message = parts
        timestamp_str = f"{date_part} {time_part}"
        try:
            timestamp = datetime.strptime(timestamp_str, self.TIMESTAMP_FORMAT)
        except ValueError:
            self._logger.warning("Malformed timestamp: %s", timestamp_str)
            return None

        return timestamp, level, ip, message

    def _in_date_range(self, ts: datetime) -> bool:
        if self.start_date and ts < self.start_date:
            return False
        if self.end_date and ts > self.end_date:
            return False
        return True

    def process_file(self, file_path: str) -> None:
        """Stream and process the given log file.

        This method does not load the file into memory and runs in O(n)
        time with respect to the number of lines.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as fh:
                for raw_line in fh:
                    parsed = self._parse_line(raw_line)
                    if parsed is None:
                        continue

                    timestamp, level, ip, message = parsed

                    # Apply filters
                    if self.level_filter and level.upper() != self.level_filter.upper():
                        continue

                    if not self._in_date_range(timestamp):
                        continue

                    # Update totals and counters
                    self.total_logs += 1
                    self.level_counts[level.upper()] += 1
                    self.ip_counts[ip] += 1

                    if level.upper() == "ERROR":
                        self.error_messages[message] += 1

                    if self.first_log_time is None or timestamp < self.first_log_time:
                        self.first_log_time = timestamp
                    if self.last_log_time is None or timestamp > self.last_log_time:
                        self.last_log_time = timestamp
        except FileNotFoundError:
            self._logger.error("File not found: %s", file_path)
            raise

    def get_stats(self) -> Dict[str, Any]:
        """Return computed statistics in a serializable structure."""
        most_common_ip = self.ip_counts.most_common(1)
        most_ip = most_common_ip[0][0] if most_common_ip else ""
        top3_errors = self.error_messages.most_common(3)

        

        first_ts = (
            self.first_log_time.strftime(self.TIMESTAMP_FORMAT)
            if self.first_log_time
            else ""
        )
        last_ts = (
            self.last_log_time.strftime(self.TIMESTAMP_FORMAT)
            if self.last_log_time
            else ""
        )

        return {
            "total": self.total_logs,
            "INFO": int(self.level_counts.get("INFO", 0)),
            "WARNING": int(self.level_counts.get("WARNING", 0)),
            "ERROR": int(self.level_counts.get("ERROR", 0)),
            "most_ip": most_ip,
            "top3_errors": top3_errors,
            "first_log_time": first_ts,
            "last_log_time": last_ts,
        }


def parse_date_input(date_str: Optional[str]) -> Optional[datetime]:
    """Parse a user-supplied date or datetime string into a datetime.

    Accepts either 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'.
    For date-only inputs, `start` will be midnight and `end` will be 23:59:59.
    """
    if not date_str:
        return None

    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {date_str}")
