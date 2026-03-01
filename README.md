# Log Analytics Engine (Python)

🚀 Log Analytics Engine (Python)

A high-performance, memory-efficient Log Analytics Engine built in Python for processing and analyzing large server log files using streaming I/O and O(n) aggregation techniques.

The engine is designed to handle high-volume log datasets (validated with 1,000,000+ entries) while maintaining stable memory usage and predictable linear performance.

📌 Features

✅ Streaming file processing (no full file loading)

✅ O(n) time complexity

✅ Log level aggregation (INFO / WARNING / ERROR)

✅ Most frequent IP detection

✅ Top 3 error message analysis (with counts)

✅ First and last timestamp extraction

✅ CLI-based filtering (level & date range)

✅ JSON export support

✅ Execution-time benchmarking

✅ Graceful handling of malformed lines

📂 Log Format

Expected log format:
```bash
YYYY-MM-DD HH:MM:SS LEVEL IP_ADDRESS Message
```
```bash
2026-01-01 10:23:41 INFO 192.168.1.10 User login successful
```
▶️ Usage
Basic analysis
```bash
python main.py --file path/to/logfile.log
```
Filter by log level
```bash
python main.py --file path/to/logfile.log --level ERROR
```

Filter by level and date range, export JSON:

```bash
python main.py --file path/to/logfile.log --level ERROR --start-date 2026-01-01 --end-date 2026-02-01 --export-json out.json
```
Export summary to JSON
```bash
python main.py --file path/to/logfile.log --export-json output.json
```

📊 Example Output
```bash
Total Logs: 1000000
INFO: 700000
WARNING: 200000
ERROR: 100000
Most Frequent IP: 192.168.1.10
Top 3 Errors:
1. Database connection failed (23000)
2. Timeout error (18000)
3. Disk full (9000)
First Log Time: 2026-01-01 00:00:00
Last Log Time: 2026-01-12 13:46:39

Processed in 4.82 seconds
```
⚙️ Performance Validation

-The engine was tested using a generated dataset of 1,000,000 log entries.

-Linear scaling behavior (O(n))

-Stable memory usage due to streaming processing

-No full-file memory load

-Efficient frequency aggregation using collections.Counter

🏗️ Architecture Overview

-analyzer.py → Core log processing and aggregation logic

-main.py → CLI interface, filtering, output formatting, benchmarking

-Separation of concerns ensures clean, maintainable structure.

🛡️ Error Handling

-Skips malformed lines

-Logs warnings for invalid entries

-Handles empty files safely

-Validates date input formats

📌 Technical Stack

-Python 3

-argparse (CLI interface)

-collections.Counter (frequency aggregation)

-datetime (timestamp processing)

-streaming file I/O
