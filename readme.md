# Log Monitoring Application

This application analyzes log files to track job execution times and identify jobs that exceed specified duration thresholds.

## Features

- Parses CSV-formatted log files
- Tracks job start and end times
- Calculates job durations
- Identifies jobs that exceed warning (5 minutes) and error (10 minutes) thresholds
- Detects incomplete and overlapping jobs
- Provides both command-line and GUI interfaces

## Dependencies

- Python 3.6+
- Tkinter (for GUI)
- Matplotlib (for visualization)

## Installation

1. Clone this repository:
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```
2. Install required dependencies:
   ```sh
   pip install matplotlib
   ```
   (Tkinter is included with most Python installations)

## Usage

### Command Line Interface

Run the following command to process log files via CLI:

```sh
python log_processor.py
```

### GUI Interface

Launch the GUI with:

```sh
python gui.py
```

The GUI allows you to:
- Select a log file using a file browser
- View job durations and statuses
- See a visual representation of job durations
- Identify problematic jobs with color highlighting

## Testing

Run the tests with:

```sh
python -m unittest test_log_processor.py
```

## Future Improvements

If I had more time, I would have implemented the following to make the application more robust:

1. **Streaming processing for large files**: Currently, the application loads the entire log file into memory, which could be problematic for very large files. A streaming approach would process the file line by line.

2. **Database integration**: For persistent storage and faster querying of large datasets.

3. **Multi-threading**: To improve performance when processing large files.

4. **More sophisticated time handling**: Currently, the application assumes all logs are from the same day. Adding date support would allow for multi-day job tracking.

5. **Log rotation support**: The ability to process multiple log files that represent rotated logs.

6. **More comprehensive error handling**: Better handling of malformed log entries and edge cases.

7. **Configuration options**: Allow users to customize warning and error thresholds.

8. **Export functionality**: Add the ability to export reports in various formats (csv, txt).

9. **Real-time monitoring**: Add support for watching log files as they're being written to.

10. **Performance metrics**: Track and display application performance statistics when processing large files.

