import os
import time

LOG_ERROR = 0
LOG_INFO = 1
LOG_DEBUG = 2
LOG_PREFIX = {
    LOG_ERROR: "[ERRO]",
    LOG_INFO: "[INFO]",
    LOG_DEBUG: "[DEBG]",
}

is_daemon = False
log_file = None
log_level = LOG_INFO

def init_log(_is_daemon, _log_level=LOG_INFO, log_file_path="/var/log/ddns.log"):
    global is_daemon, log_file, log_level
    is_daemon = _is_daemon
    
    if is_daemon:
        if not os.path.exists(log_file_path):
            fp = open(log_file_path, "w")
            fp.close()
        log_file = open(log_file_path, "a")
    log_level = _log_level

def msg(level, fmt, *args):
    if level > log_level:
        return
    buf = LOG_PREFIX[level] + ' '
    if not isinstance(fmt, str):
        fmt = str(fmt)
    if len(args) > 0:
        buf += fmt.format(*args)
    else:
        buf += fmt
    if log_file:
        buf = time.ctime()  + ' ' + buf + '\n'
        log_file.write(buf)
        log_file.flush()
    else:
        print(buf)

def error(fmt, *args):
    msg(LOG_ERROR, fmt, *args)

def info(fmt, *args):
    msg(LOG_INFO, fmt, *args)

def debug(fmt, *args):
    msg(LOG_DEBUG, fmt, *args)
