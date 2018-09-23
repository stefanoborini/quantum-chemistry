import logging
import logging.handlers

_inited = False

def _init():
    global _inited
    if _inited:
        return
    rootLogger = logging.getLogger('')
    rootLogger.setLevel(logging.DEBUG)
    socketHandler = logging.handlers.SocketHandler('localhost', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    rootLogger.addHandler(socketHandler)
    _inited = True


def logger(logger_name):
    global _inited
    if not _inited:
        _init()

    logger = logging.getLogger(logger_name)
    return logger
    
    

