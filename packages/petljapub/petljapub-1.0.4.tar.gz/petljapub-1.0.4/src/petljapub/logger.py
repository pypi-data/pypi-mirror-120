import sys

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# 0 - quit
# 1 - only errors
# 2 - only errors and warnings
# 3 - errors, warings and info
# >3 - more details
_verbosity = 3

_warn_stream = sys.stderr
_error_stream = sys.stderr
_info_stream = sys.stderr

def err(*str):
    if _verbosity > 0:
        print(f"{colors.FAIL}ERROR:{colors.ENDC}", *str, file=_error_stream)

def error(*str):
    err(*str)
        
def warn(*str):
    if _verbosity > 1:
        print(f"{colors.WARNING}WARNING:{colors.ENDC}", *str, file=_warn_stream)

def warning(*str):
    warn(*str)

def info(*str, verbosity=3):
    if _verbosity >= verbosity:
        print(f"{colors.OKGREEN}INFO:{colors.ENDC}", *str, file=_info_stream)
