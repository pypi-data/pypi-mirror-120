import logging
import os

from . import makeFolder

from .print import (FOREGROUND_DARKPINK, FOREGROUND_DARKRED,
                    FOREGROUND_DARKYELLOW, resetPrintColor, setPrintColor)

_loggerName = 'beniutils'

_countWarning = 0
_countError = 0
_countCritical = 0


def initLogger(loggerName=None, loggerLevel=None, logFile=None):
    LOGGER_FORMAT = '%(asctime)s %(levelname)-1s %(message)s', '%Y-%m-%d %H:%M:%S'
    LOGGER_LEVEL = loggerLevel or logging.INFO
    LOGGER_LEVEL_NAME = {
        logging.DEBUG: 'D',
        logging.INFO: '',
        logging.WARNING: 'W',
        logging.ERROR: 'E',
        logging.CRITICAL: 'C',
    }

    if loggerName:
        global _loggerName
        _loggerName = loggerName

    logger = logging.getLogger(_loggerName)
    logger.setLevel(LOGGER_LEVEL)
    for loggingLevel, value in LOGGER_LEVEL_NAME.items():
        logging.addLevelName(loggingLevel, value)

    loggerFormatter = logging.Formatter(*LOGGER_FORMAT)

    class CustomStreamHandler(logging.StreamHandler):
        def emit(self, record):
            try:
                msg = self.format(record) + self.terminator
                # issue 35046: merged two stream.writes into one.
                func = self.stream.write
                if record.levelno == logging.WARNING:
                    global _countWarning
                    _countWarning += 1
                    setPrintColor(FOREGROUND_DARKYELLOW)
                elif record.levelno == logging.ERROR:
                    global _countError
                    _countError += 1
                    setPrintColor(FOREGROUND_DARKRED)
                elif record.levelno == logging.CRITICAL:
                    global _countCritical
                    _countCritical += 1
                    setPrintColor(FOREGROUND_DARKPINK)
                func(msg)
                resetPrintColor()
                self.flush()
            except RecursionError:  # See issue 36272
                raise
            except Exception:
                self.handleError(record)

    loggerHandler = CustomStreamHandler()
    loggerHandler.setFormatter(loggerFormatter)
    loggerHandler.setLevel(LOGGER_LEVEL)
    logger.addHandler(loggerHandler)

    if logFile:
        makeFolder(os.path.dirname(logFile))
        fileLoggerHandler = logging.FileHandler(logFile)
        fileLoggerHandler.setFormatter(loggerFormatter)
        fileLoggerHandler.setLevel(LOGGER_LEVEL)
        logger.addHandler(fileLoggerHandler)


def debug(msg, *args, **kwargs):
    logging.getLogger(_loggerName).debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    logging.getLogger(_loggerName).info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    logging.getLogger(_loggerName).warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    logging.getLogger(_loggerName).error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    logging.getLogger(_loggerName).critical(msg, *args, **kwargs)


def getCountWarning():
    return _countWarning


def setCountWarning(value):
    global _countWarning
    _countWarning = value


def getCountError():
    return _countError


def setCountError(value):
    global _countError
    _countError = value


def getCountCritical():
    return _countCritical


def setCountCritical(value):
    global _countCritical
    _countCritical = value
