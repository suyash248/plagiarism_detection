__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import logging

Logger = logging.getLogger('Plagiarism-Detection')

logger_names = ('sqlalchemy.engine.base.Engine')
for logger_name in logger_names:
    _logger = logging.getLogger(logger_name)
    for handler in _logger.handlers:
         Logger.addHandler(handler)
