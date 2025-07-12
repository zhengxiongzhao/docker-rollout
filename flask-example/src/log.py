import logging
import os

class CustomStyleFormatter(logging.Formatter):
    """A custom log formatter that mimics default log format."""
    
    def format(self, record):
        clean_thread_name = record.threadName.split('(')[0].strip()
        
        # Abbreviate the logger name (e.g., 'app.service.logic' -> 'a.s.logic')

        short_name = record.name
        if len(record.name) > 20:
            name_parts = record.name.split('.')
            if len(name_parts) > 1:
                short_name = '.'.join([p[0] for p in name_parts[:-1]] + [name_parts[-1]])
        
        # Add custom fields to the record
        record.short_logger_name = f"{short_name:<20}"
        record.pid = os.getpid()
        record.levelname = f"{record.levelname:<5}"
        record.clean_thread_name = f"{clean_thread_name:<10}"

        # Define the final format string
        log_format = (
            "%(asctime)s.%(msecs)03d %(levelname)s %(pid)d - [%(clean_thread_name)s] "
            "%(short_logger_name)s [%(lineno)d]: %(message)s"
        )
        
        # Create a new formatter and apply it
        formatter = logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

log = logging.getLogger('werkzeug')
log.disabled = True

logger_style_handler = logging.StreamHandler()
logger_style_handler.setFormatter(CustomStyleFormatter())

