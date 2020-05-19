#!/usr/bin/python3
import sys
from .file_signer import sign_the_file
from .parameter_handler import ParameterHandler

if __name__ == "__main__":

    code = sign_the_file(ParameterHandler().read_parameters(sys.argv[1:]))

    if code is None:
        code = 0

    sys.exit(code)
