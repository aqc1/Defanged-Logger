import functools
import logging

class Logger:
    """
    Class designed to produce logs with automatically defanged resources
    Wrapper around logging class

    Can pass in the following as a resource
    - NoneType
    - str
    - list of str

    example)
        log = Logger(log_location="logs/project.log")
        log.info(
            message="Some format here {}"
            resource="http://example.com"
        )

    log_location (str)
        Where logs are to be written to
    log_format (str)
        Format in which events are logged
    log_level (int)
        Current level of minimum logs being written
        DEBUG, INFO, WARNING, ERROR, CRITICAL
    log (logging.Logger)
        logging.Logger object
    levels (list)
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
                resource = kwargs['resource']
                if type(resource) == str:
                    defanged = resource.replace("http", "hxxp")
                    defanged = defanged.replace("://", "[://]")
                    defanged = defanged.replace(".", "[.]")
                    defanged = f"\"{defanged}\""
                    return func(self, message=kwargs['message'], resource=defanged)
                else:
                    defanged_resources = list() 
                    for item in resource:
                        defanged = item.replace("http", "hxxp")
                        defanged = defanged.replace("://", "[://]")
                        defanged = defanged.replace(".", "[.]")
                        defanged = f"\"{defanged}\""
                        defanged_resources.append(defanged)
                    return func(self, message=kwargs['message'], resource=defanged_resources)
            except:
                return func(self, message=kwargs['message'], resource=None)
        return wrapper

    @defang
    def debug(self, message: str, resource=None):
        """Logging for debugging: Non-production"""
        if type(resource) == list:
            self.log.debug(message.format(*resource))
        else:
            self.log.debug(message.format(resource))

    @defang
    def info(self, message: str, resource=None):
        """Logging informational information"""
        if type(resource) == list:
            self.log.info(message.format(*resource))
        else:
            self.log.info(message.format(resource))


    @defang
    def warning(self, message: str, resource=None):
        """Logging warnings"""
        if type(resource) == list:
            self.log.warning(message.format(*resource))
        else:
            self.log.warning(message.format(resource))


    @defang
    def error(self, message: str, resource=None):
        """Logging error events"""
        if type(resource) == list:
            self.log.error(message.format(*resource))
        else:
            self.log.error(message.format(resource))

    @defang
    def critical(self, message: str, resource=None):
        """Logging critical events"""
        if type(resource) == list:
            self.log.critical(message.format(*resource))
        else:
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

