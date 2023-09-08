import os
import sys

from loguru import logger as logging

from config import settings


def mkdir(path: str) -> bool:
    path = path.rstrip("/")
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
        return True
    else:
        return False


class Logger:
    def __init__(self, log_name: str = settings.log_name):
        root_path = settings.site_root
        log_path = f"{root_path}/logs/"
        mkdir(log_path)
        log_file_path = f"{root_path}/logs/{log_name}"
        self.logger = logging
        self.logger.remove()
        self.logger.add(
            sys.stdout,
            level=settings.stdout_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level:8}</level> | "
                   "<magenta>{module}.{function}:{line}</magenta> - "
                   "<level>{message}</level>",
            diagnose=False,
            enqueue=False
        )
        self.logger.add(
            log_file_path,
            level=settings.file_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | "
                   "{level:8} | "
                   "{module}.{function}:{line} - "
                   "{message}",
            diagnose=False,
            rotation=settings.rotation,
        )

    def get_logger(self):
        return self.logger


logger = Logger().get_logger()

if __name__ == "__main__":
    logger.debug("debug")
    logger.info("test")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
