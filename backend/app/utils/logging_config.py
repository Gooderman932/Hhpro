"""
Enhanced logging configuration for production.

Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.
"""
import sys
import os
from pathlib import Path
from typing import Optional

try:
    from loguru import logger
    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False
    # Fallback to standard logging if loguru is not available
    import logging
    logger = logging.getLogger(__name__)


def setup_logging(
    log_level: str = "INFO",
    log_dir: Optional[str] = None,
    environment: str = "production"
):
    """
    Configure logging with separate files for different levels and console output.
    
    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (default: ./logs)
        environment: Environment name (development, staging, production)
    """
    if not LOGURU_AVAILABLE:
        # Fallback to standard logging
        log_file = os.path.join(log_dir if log_dir else '.', 'app.log')
        logging.basicConfig(
            level=getattr(logging, log_level, logging.INFO),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(log_file) if log_dir else logging.StreamHandler(sys.stdout)
            ]
        )
        logging.info(f"Using standard logging (loguru not available) - Level: {log_level}")
        return logging.getLogger(__name__)
    
    # Remove default handler
    logger.remove()
    
    # Set log directory
    if log_dir is None:
        log_dir = os.getenv("LOG_DIR", "./logs")
    
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Log format with colors for console
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # Log format for files (no colors)
    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    )
    
    # Console logging (with colors in development)
    if environment == "development":
        logger.add(
            sys.stdout,
            format=console_format,
            level=log_level,
            colorize=True,
            backtrace=True,
            diagnose=True,
        )
    else:
        # Production console logging (no colors, less verbose)
        logger.add(
            sys.stdout,
            format=file_format,
            level=log_level,
            colorize=False,
            backtrace=False,
            diagnose=False,
        )
    
    # Info log file - general application logs
    logger.add(
        log_path / "info.log",
        format=file_format,
        level="INFO",
        rotation="100 MB",  # Rotate when file reaches 100MB
        retention="30 days",  # Keep logs for 30 days
        compression="zip",  # Compress rotated logs
        backtrace=True,
        diagnose=True,
        enqueue=True,  # Thread-safe logging
    )
    
    # Error log file - errors and critical issues only
    logger.add(
        log_path / "error.log",
        format=file_format,
        level="ERROR",
        rotation="100 MB",
        retention="90 days",  # Keep error logs longer
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True,
    )
    
    # Access log file - API requests and responses (if needed)
    logger.add(
        log_path / "access.log",
        format=file_format,
        level="INFO",
        rotation="100 MB",
        retention="30 days",
        compression="zip",
        filter=lambda record: "access" in record["extra"],
        enqueue=True,
    )
    
    # Debug log file - verbose logging for debugging (only in development)
    if environment == "development":
        logger.add(
            log_path / "debug.log",
            format=file_format,
            level="DEBUG",
            rotation="50 MB",
            retention="7 days",  # Keep debug logs for shorter period
            compression="zip",
            backtrace=True,
            diagnose=True,
            enqueue=True,
        )
    
    logger.info(f"Logging initialized - Level: {log_level}, Environment: {environment}")
    logger.info(f"Log directory: {log_path.absolute()}")
    
    return logger


def get_logger(name: str):
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Module name (typically __name__)
    
    Returns:
        Logger instance
    """
    return logger.bind(name=name)


def log_api_access(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None
):
    """
    Log API access with structured data.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        path: Request path
        status_code: HTTP status code
        duration_ms: Request duration in milliseconds
        user_id: User ID if authenticated
        ip_address: Client IP address
    """
    logger.bind(access=True).info(
        f"{method} {path} - {status_code} - {duration_ms:.2f}ms - "
        f"User: {user_id or 'anonymous'} - IP: {ip_address or 'unknown'}"
    )


def log_exception(exc: Exception, context: str = ""):
    """
    Log exception with full traceback.
    
    Args:
        exc: Exception instance
        context: Additional context about where the exception occurred
    """
    if context:
        logger.exception(f"Exception in {context}: {exc}")
    else:
        logger.exception(f"Exception: {exc}")


# Example usage patterns for different scenarios
def example_usage():
    """Example usage patterns (for documentation purposes)."""
    
    # Basic logging
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Structured logging with context
    logger.info("User logged in", user_id=123, ip="192.168.1.1")
    
    # Exception logging
    try:
        raise ValueError("Something went wrong")
    except Exception as e:
        log_exception(e, "user authentication")
    
    # API access logging
    log_api_access(
        method="GET",
        path="/api/v1/projects",
        status_code=200,
        duration_ms=45.67,
        user_id=123,
        ip_address="192.168.1.1"
    )
    
    # Module-specific logger
    module_logger = get_logger(__name__)
    module_logger.info("This log includes the module name")


if __name__ == "__main__":
    # Initialize logging for testing
    setup_logging(log_level="DEBUG", environment="development")
    
    # Test different log levels
    logger.debug("Debug message - detailed information for diagnostics")
    logger.info("Info message - general informational messages")
    logger.warning("Warning message - warning about potential issues")
    logger.error("Error message - error that needs attention")
    
    # Test exception logging
    try:
        1 / 0
    except Exception as e:
        log_exception(e, "division test")
    
    # Test access logging
    log_api_access("GET", "/api/v1/test", 200, 42.5, 1, "127.0.0.1")
    
    logger.info("Logging configuration test completed")
