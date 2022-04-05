#!/usr/bin/env python
# @Author: Niccolò Bonacchi
# @Creation_Date: Friday, January 11th 2019, 2:04:42 pm
# @Editor: Michele Fabbri
# @Edit_Date: 2022-02-01
"""
Configuration for logging
"""
import logging

LOGLEVEL = logging.DEBUG


def logger_config(name=None):
    import logging

    import colorlog

    """
        Setup the logging environment
    """
    lc_log = logging.getLogger() if not name else logging.getLogger(name)
    lc_log.setLevel(logging.INFO)
    format_str = "%(asctime)s.%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    cformat = "%(log_color)s" + format_str
    colors = {
        "DEBUG": "green",
        "INFO": "cyan",
        "WARNING": "bold_yellow",
        "ERROR": "bold_red",
        "CRITICAL": "bold_purple",
    }
    formatter = colorlog.ColoredFormatter(cformat, date_format, log_colors=colors)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    lc_log.addHandler(stream_handler)
    return lc_log


log = logger_config(name="iblrig")
log.setLevel(LOGLEVEL)
