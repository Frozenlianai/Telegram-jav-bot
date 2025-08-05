import logging
import sys

# A more detailed formatter
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s"

class Logger:
    """日志记录器"""

    def __init__(self, path_log_file: str, log_level=logging.INFO):
        """
        Initializes the logger, preventing duplicate handlers.

        :param str path_log_file: Path to the log file.
        :param int log_level: Logging level, defaults to INFO.
        """
        self.logger = logging.getLogger()
        
        # Clear existing handlers to prevent duplicate logs
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.setLevel(log_level)
        formatter = logging.Formatter(LOG_FORMAT)

        # File handler
        try:
            file_handler = logging.FileHandler(path_log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            # If file handler fails, log to console and continue
            self.logger.error(f"无法创建日志文件处理器: {e}")

        # Stream handler (console)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
