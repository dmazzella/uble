import sys

_stream = sys.stderr

CRITICAL = 50
ERROR    = 40
WARNING  = 30
INFO     = 20
DEBUG    = 10
NOTSET   = 0

_level_dict = {
    CRITICAL: "CRIT",
    ERROR: "ERROR",
    WARNING: "WARN",
    INFO: "INFO",
    DEBUG: "DEBUG",
}

class Logger(object):

    def __init__(self, name):
        self.level = NOTSET
        self.name = name or "root"

    def _level_str(self, level):
        global _level_dict
        if level in _level_dict:
            return _level_dict[level]
        return "LVL" + str(level)

    def log(self, level, msg, *args, **kwargs):
        global _level, _stream
        if level >= (self.level or _level):
            log_format_list = [self._level_str(level), self.name]
            log_format_msg = ":".join(map(str, log_format_list))
            try:
                print(log_format_msg, msg % args, file=_stream)
            except TypeError as te:
                print(
                    ("--- Logging error ---\n"
                     "{!r}\n"
                     "Message: {!r}\n"
                     "Arguments: {!r}".format(te, msg, args)
                    ), file=_stream)
            if _stream not in (sys.stderr, sys.stdout) \
                and hasattr(_stream, "flush"):
                _stream.flush()

    def debug(self, msg, *args, **kwargs):
        self.log(DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log(INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.log(WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log(ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log(CRITICAL, msg, *args, **kwargs)

    def exc(self, e, msg, *args): 
        self.log(ERROR, msg, *args)
        sys.print_exception(e, _stream)

    def exception(self, msg, *args):
        e = None
        if hasattr(sys, 'exc_info'):
            e = sys.exc_info()[1]
        self.exc(e, msg, *args)

_level = INFO
_loggers = {}

def getLogger(name=""):
    global _loggers
    if name in _loggers:
        return _loggers[name]
    l = Logger(name)
    _loggers[name] = l
    return l

def info(msg, *args):
    getLogger(None).info(msg, *args)

def debug(msg, *args):
    getLogger(None).debug(msg, *args)

def basicConfig(level=INFO, filename=None, stream=None, format=None):
    global _level, _stream
    _level = level
    if stream:
        _stream = stream
    if filename is not None:
        raise AttributeError("filename")
    if format is not None:
        raise AttributeError("format")
