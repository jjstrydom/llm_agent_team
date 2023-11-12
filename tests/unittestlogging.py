import unittest
import logging
import traceback
from pprint import pformat

class TestCaseLogging(unittest.TestCase):
    def __init__(self, *args):
        super(TestCaseLogging, self).__init__(*args)
        for name, method in unittest.TestCase.__dict__.items():
            if callable(method) and name.startswith('assert') and ('_' not in name):
                setattr(unittest.TestCase, name, self.log_data(method))

    @staticmethod
    def get_traceback():
        return '\n'.join([a for a in traceback.format_exc().split('\n') if 'unittestlogging.py' not in a])

    def log_all_arguments(self, args, data):
        for arg in args:
            logging.warning(arg)
        if data:
            logging.warning(pformat(data))

    def log_data(self, func):
        def wrapper(self, *args, **kwargs):
            data = kwargs.pop('data', None)
            try:
                func(self, *args, **kwargs)
                if self.log_successes:
                    logging.error("SUCCESS")
                    self.log_all_arguments(args, data)
            except Exception as e:
                if self.log_failures:
                    logging.error("FAILURE")
                    self.log_all_arguments(args, data)
                    logging.error(self.get_traceback())
                raise
        return wrapper

    def setup_logging(self, log_failures:bool=True, log_successes:bool=False, filename:str = 'logs.log', level=logging.DEBUG):
        self.log_failures = log_failures
        self.log_successes = log_successes
        logging.basicConfig(filename=filename, encoding='utf-8', level=level, filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
