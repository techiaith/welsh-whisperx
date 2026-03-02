import os
import logging
from pathlib import Path
from datetime import datetime

RECORDINGS_DIR = "/recordings"

class STTLogger:
    """Logger for speech-to-text transcription jobs.

    Creates and manages log files for each stt_id in the shared recordings folder.
    Both API and worker containers can write to these logs.
    """

    def __init__(self, stt_id: str):
        self.stt_id = stt_id
        self.log_file_path = os.path.join(RECORDINGS_DIR, f"{stt_id}.log")

        # Create a logger instance for this stt_id
        self.logger = logging.getLogger(f"stt.{stt_id}")
        self.logger.setLevel(logging.INFO)

        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # Create file handler
        file_handler = logging.FileHandler(self.log_file_path, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # Create formatter (excluding %(name)s to avoid showing stt.{uuid} in logs)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add handler to logger
        self.logger.addHandler(file_handler)

        # Prevent propagation to root logger
        self.logger.propagate = False

    def info(self, message: str):
        """Log an info message."""
        self.logger.info(message)

    def error(self, message: str):
        """Log an error message."""
        self.logger.error(message)

    def warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)

    def debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)

    def close(self):
        """Close and cleanup handlers."""
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)


def get_logger(stt_id: str) -> STTLogger:
    """Factory function to create/get a logger for a given stt_id."""
    return STTLogger(stt_id)
