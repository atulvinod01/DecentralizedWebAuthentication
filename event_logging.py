# event_logging.py
import logging
from logging.handlers import RotatingFileHandler
import json
from flask import request, session

def setup_custom_logger(name):
    """Setup and return a custom logger for security events."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels of log messages

    # Log file handler with rotation
    log_file_handler = RotatingFileHandler('security_logs.log', maxBytes=10**6, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_file_handler.setFormatter(formatter)

    logger.addHandler(log_file_handler)

    return logger

# Initialize the logger
security_logger = setup_custom_logger('SecurityLogger')

def log_event(message, level='info'):
    """Log an event at the specified level with additional request information."""
    if level == 'info':
        security_logger.info(message)
    elif level == 'warning':
        security_logger.warning(message)
    elif level == 'error':
        security_logger.error(message)
    elif level == 'debug':
        security_logger.debug(message)

def log_request():
    """Function to log detailed request data, used as a before_request action in Flask."""
    request_data = {
        'source_ip': request.remote_addr,
        'destination_ip': request.host,
        'user_agent': request.user_agent.string,
        'endpoint': request.endpoint,
        'method': request.method,
        'data': request.get_json() or request.data,
        'user': session.get('user', 'Anonymous')
    }
    log_event(json.dumps(request_data), 'debug')
