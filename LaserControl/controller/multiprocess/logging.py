import os


def log_debug(msg, prefix="LAS Thread"):
    print(f"DBG  | [{prefix}/{os.getpid()}]: {msg}")


def log_error(msg, prefix="LAS Thread"):
    print(f"ERR  | [{prefix}/{os.getpid()}]: {msg}")


def log_info(msg, prefix="LAS Thread"):
    print(f"INF  | [{prefix}/{os.getpid()}]: {msg}")


def log_warning(msg, prefix="LAS Thread"):
    print(f"WARN | [{prefix}/{os.getpid()}]: {msg}")