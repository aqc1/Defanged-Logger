import functools
import logging

class Logger:
    """
    Class designed to produce logs with automatically defanged resources
    Wrapper around logging class

    example)
        log = Logger(log_location="logs/project.log")
        log.info(
            message="Some format here {}"
            resource="http://example.com"
        )

    log_location (str)
        Where logs are to be written to
    log_format
        Format in which events are logged
    log_level
        Current level of minimum logs being written
        DEBUG, INFO, WARNING, ERROR, CRITICAL
    log
        logging.Logger object
    levels
        Available log levels
    """

    def __init__(self, log_location: str):
        self.log_location = log_location
        self.log_format = "%(asctime)s [%(levelname)s] - %(filename)s [Line: %(lineno)d]: %(message)s"
        self.log_level = logging.INFO
        logging.basicConfig(
            filename=self.log_location,
            format=self.log_format,
            level=self.log_level
        )
        self.log = logging.getLogger(__name__)
        self.levels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL
        ]

    def defang(func):
        """Decorator for defanging resource locations"""
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                protocol, host = kwargs['resource'].split("://")
                defanged = f"{protocol.replace('t', 'x').replace('T', 'x')}://{host}"
                defanged = defanged.replace("://", "[://]")
                defanged = defanged.replace(".", "[.]")
                return func(self, message=kwargs['message'], resource=f"\"{defanged}\"")
            except:
                return func(self, message=kwargs['message'], resource=None)
        return wrapper

    @defang
    def debug(self, message: str, resource=None):
        """Logging for debugging: Non-production"""
        self.log.debug(message.format(resource))

    @defang
    def info(self, message: str, resource=None):
        """Logging informational information"""
        self.log.info(message.format(resource))

    @defang
    def warning(self, message: str, resource=None):
        """Logging warnings"""
        self.log.warning(message.format(resource))

    @defang
    def error(self, message: str, resource=None):
        """Logging error events"""
        self.log.error(message.format(resource))

    @defang
    def critical(self, message: str, resource=None):
        """Logging critical events"""
        self.log.critical(message.format(resource))

    def lower_log_level(self):
        """Lower logging level"""
        index = self.levels.index(self.log_level)
        if index != 0:
            self.log_level = self.levels[index - 1]
            self.log.setLevel(self.log_level)

    def raise_log_level(self):
        """Raise logging level"""
        index = self.levels.index(self.log_level)
        if index != (len(self.levels) - 1):
            self.log_level = self.levels[index + 1]
            self.log.setLevel(self.log_level)

