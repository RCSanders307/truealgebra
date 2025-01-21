# -*- coding: utf-8 -*-
"""
Create TALogger class to handle TrueAlgebra user errors.

This module is not complete and requires more work and testing.
There will be four options for a user with a TALogger instance.

print
    An error message is printed out (on stdout). This is the default, which is
    ideal for users in interactive session such as Jupyter or ipython.
    The user will immediately see the error message printed on their screen
    after the error occurs.

    TrueAlgebra is designed for use in interactive sessions, or in the
    creation of documents using Jupyter or sphinxi (with ipython directives)

makeexception
    A TrueAlgebraError exception is raised.
    Intended for use in TrueAlgebra scripts.

mute
    No printing or raising TrueAlgebraError exceptions.
    This feature is not fully develpoed.

logging
    error messages are written to files using python logging module.
    This feature is not fully develpoed.
"""
import logging
import sys

logger = logging.getLogger('TrueAlgebra error logger')
stderr_handler = logging.StreamHandler(sys.stderr)
logger.handlers = [stderr_handler]
logger.setLevel(logging.ERROR)

#This needs to be integrated with what is belo
class TrueAlgebraError(Exception):
    pass


def print_error(msg):
    print('TRUEALGEBRA ERROR!\n' + msg)


def mute(msg):
    pass


# log_dict can probably be done away with
log_dict = dict()
log_dict['error'] = logger.error
log_dict['exception'] = logger.exception
log_dict['print'] = print_error
log_dict['mute'] = mute


class TrueAlgebraError(Exception):
    """Raise when TrueAlgebra Error is to cause session to crash and burn."""


class TALogger:
    def __init__(self, log_dict, initial):
        self.log_dict = log_dict
        self.choice = log_dict[initial]

    def set_choice(self, choice):
        self.choice = self.log_dict[choice]

    make_exception = False

    def set_make_exception(self):
        self.make_exception = True

    def clear_make_exception(self):
        self.make_exception = False

    def log(self, msg):
        complete_msg = 'TRUEALGEBRA ERROR!\n' + msg
        if self.make_exception:
            raise TrueAlgebraError(complete_msg)
        else:
            print(complete_msg)


ta_logger = TALogger(log_dict, 'print')
