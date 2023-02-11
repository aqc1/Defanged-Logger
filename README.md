# Defanged-Logger
Very simple wrapper around the Python logging module to attempt to automatically defang resource locations

## How does this defang resources?
- A few items in resource locations are modified
    - Protocols: http => hxxp, ftp => fxp, etc.
    - Other: :// => [://], . => [.]

## How to use the logging library
- _Very_ similiar to the standard logging library with a few "quirks"
- Pass in a file location by default
- Default logging level is equivalent to `logging.INFO`
- Log levels are identical to those in the traditional logging library
- Example usage below:

```
from logger import Logger

# Instantiate
log = Logger(log_location="logs/report.log")

# The following code will create a log with the following message
# timestamps [log level] - logger.py [Line: line #]: Log message goes here, don't forget to add "hxxp[://]example[.]com to format in a resource
log.info(
    message="Log message goes here, don't forget to add {} to format in a resource,
    resource="http://example.com
)

# Raise log level by 1
log.raise_log_level()

# Lower log level by 1
log.lower_log_level()
```
