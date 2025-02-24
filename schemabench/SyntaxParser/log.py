
import logging
import colorlog


logger = logging.getLogger("SyntaxParser")
logger.setLevel(logging.CRITICAL)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

formatter = colorlog.ColoredFormatter(fmt='%(log_color)s%(levelname)s - %(name)s - %(message)s',
                          log_colors={
                              'DEBUG':    'white',
                              'INFO':     'green',
                              'WARNING':  'yellow',
                              'ERROR':    'red',
                              'CRITICAL': 'red,bg_white',
                          })



console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
