import time


class Logger:
    # File where all logs will be stored
    LOG_FILE = "logs.txt"

    @staticmethod
    def _write(level, message):
        # Get current timestamp in readable format
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Format the log line with timestamp, level, and message
        log_line = f"[{timestamp}] [{level}] {message}\n"

        # Open log file in append mode ("a") so we don't overwrite existing logs
        # encoding="utf-8" ensures proper handling of all characters
        with open(Logger.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)

    @staticmethod
    def log(message):
        # Write a normal log message to file
        Logger._write("LOG", message)

        # Also print it to the console for immediate feedback
        print(f"[LOG] {message}")

    @staticmethod
    def error(message):
        # Write an error message to file
        Logger._write("ERROR", message)

        # Also print it to the console (helps debugging)
        print(f"[ERROR] {message}")