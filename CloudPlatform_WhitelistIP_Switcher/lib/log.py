#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
create_author : Bilery Zoo(bilery.zoo@gmail.com)
create_time   : 2019-09-05
program       : *_* log logging module *_*
"""


import os
import re
import sys
import logging
import functools


class LOG(object):
    """
    Log logging definition.
    """

    def __init__(self, level=logging.INFO, stream=sys.stdout, filemode='a',
                 filename=re.search("/.*/", os.path.dirname(os.path.abspath(__file__))).group() + "log",
                 datefmt="%Y-%m-%d %H:%M:%S",
                 format="%(asctime)s\t%(levelname)s\t< Module: %(module)s, Function: %(funcName)s >\t%(message)s",
                 **kwargs):
        """
        LOG init.
        :param level: arg pass to standard library logging.basicConfig().
        :param stream: arg pass to standard library logging.basicConfig().
        :param filemode: arg pass to standard library logging.basicConfig().
        :param filename: arg pass to standard library logging.basicConfig().
        :param datefmt: arg pass to standard library logging.basicConfig().
        :param format: arg pass to standard library logging.basicConfig().
        :param kwargs: arg pass to standard library logging.basicConfig().
        """
        self.level = level
        self.stream = stream
        self.filename = filename
        self.filemode = filemode
        self.datefmt = datefmt
        self.format = format
        self.kwargs = kwargs

    def logger(self, name=__name__):
        """
        Logger object generates.
        :param name: Logger name(parameters pass to standard library logging.getLogger()).
        :return: Logger object.
        """
        args = {
            "level": self.level,
            "stream": self.stream,
            "filename": self.filename,
            "filemode": self.filemode,
            "datefmt": self.datefmt,
            "format": self.format,
        }
        try:
            if self.stream and self.filename:
                del args["stream"]
        except KeyError:
            pass
        logging.basicConfig(**args, **self.kwargs)
        return logging.getLogger(name)


def raise_log(raised_except, msg=''):
    """
    Raise exception by hand to escape error exit caused by built-in [raise].
    :param raised_except: Exception object.
    :param msg: Exception feedback message.
    :return: Python's built-in exit code.
        Output Exception of [raised_except].
    """
    try:
        raise raised_except(msg)
    except raised_except as E:
        logging.exception(E)


def log(logger=None, exc_msg='', if_exit=False, exit_msg='', result_check=False, check_except=None, check_msg=''):
    """
    Log logging decorator function.
    :param logger: Logger object(see also logging.getLogger()).
    :param exc_msg: extra message to return when exceptions catch.
    :param if_exit: Boolean.
        Whether to exit or not when catching exception.
    :param exit_msg: extra message to return when exceptions catch and exit.
    :param result_check: Boolean.
        Whether or not to check Python's False status result of [func]'s return.
    :param check_except: Exception object to raise when [result_check].
    :param check_msg: Exception feedback message to return when [result_check].
    :return: decorated function [func]'s return.
    """
    if not logger:
        logger = LOG().logger()

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            try:
                result = func(*args, **kwargs)
            except BaseException:
                logger.exception(exc_msg)
                if if_exit:
                    sys.exit(exit_msg)
            finally:
                if result_check:
                    if not result:
                        raise_log(check_except, check_msg)
                return result
        return wrapper
    return decorator
