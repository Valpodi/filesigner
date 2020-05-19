"""Handle command line input to and create parameters for file_signer.py"""
import argparse
import sys
import os


class ParameterHandler(object):
    """Handles the parameters given as arguments to the programme"""
    def __init__(self):
        self.parameters = {}

    def read_parameters(self, arguments):
        """
        Reads the command line parameters given to this program
        and places them in a dictionary
        """
        parameter_size_limits = {'four_byte_max': (2**32)-1,
                                 'four_byte_min': 0,
                                 'thirtytwo_byte_max': int('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 16) -1,
                                 'thirtytwo_byte_min': 0,
                                 'filename_max': 63,
                                 'filename_min': 1,
                                 'format_max': 2,
                                 'format_min': 0}

        parser = argparse.ArgumentParser(
            description="""Sign a file using the 'Release Control' process""")
        parser.add_argument("-J", "--filename",
                            help="Specify the file to be signed",
                            default='testfile.txt')
        parser.add_argument("-K", "--uniqueid",
                            help="Specify the shared unique id <hex number, max size 32 bytes>",
                            default='0101010101010101010101010101010101010101010101010101010101010101')
        parser.add_argument("-R", "--regtoken",
                            help="Specify the registration token <hex number, max size 32 bytes>",
                            default='11')
        parser.add_argument("-V", "--version",
                            help="Specify the 'Release Control' version <int>",
                            default=1)
        parser.add_argument("-S", "--size",
                            help="Specify the maximum file size <bytes>",
                            default=0)
        parser.add_argument("-F", "--format",
                            help="Specify the file format allowed to egress "
                                 "<0 for all, 1 for rYAML, 2 for BMP>",
                            default=0)
        parser.add_argument("-Ts1", "--sessionvalidfrom",
                            help="Specify the Session ID 'validfrom' time <unix uint32>",
                            default=0)
        parser.add_argument("-Ts2", "--sessionvalidto",
                            help="Specify the Session ID 'validto' time <unix uint32>",
                            default=(2**32)-1)
        parser.add_argument("-Tm1", "--filevalidfrom",
                            help="Specify the signed file 'valid from' time <unix uint32>",
                            default=0)
        parser.add_argument("-Tm2", "--filevalidto",
                            help="Specify the signed file 'valid to' time <unix uint32>",
                            default=(2**32)-1)
        parser.add_argument("-N", "--nonce",
                            help="Specify the nonce for the file <int>",
                            default=1)
        parser.add_argument("-O", "--output",
                            help="Specify the outputfile full path name",
                            default=None)

        args = parser.parse_args(arguments)

        self.parameters['In_Path'], args.filename = os.path.split(args.filename)

        for param in vars(args):
            value = (getattr(args, param))
            if value is '':
                sys.exit("Empty arguments are invalid")

        mapping = [
            ['J',   args.filename,              parameter_size_limits['filename_min'],       parameter_size_limits['filename_max'],       len],
            ['K',   int(args.uniqueid, 16),     parameter_size_limits['thirtytwo_byte_min'], parameter_size_limits['thirtytwo_byte_max'], int],
            ['R',   int(args.regtoken, 16),     parameter_size_limits['thirtytwo_byte_min'], parameter_size_limits['thirtytwo_byte_max'], int],
            ['V',   int(args.version),          parameter_size_limits['four_byte_min'],      parameter_size_limits['four_byte_max'],      int],
            ['S',   int(args.size),             parameter_size_limits['four_byte_min'],      parameter_size_limits['four_byte_max'],      int],
            ['F',   int(args.format),           parameter_size_limits['four_byte_min'],      parameter_size_limits['four_byte_max'],      int],
            ['Ts1', int(args.sessionvalidfrom), parameter_size_limits['four_byte_min'],      parameter_size_limits['four_byte_max'],      int],
            ['Ts2', int(args.sessionvalidto),   parameter_size_limits['four_byte_min'],      parameter_size_limits['four_byte_max'],      int],
            ['Tm1', int(args.filevalidfrom),    parameter_size_limits['four_byte_min'],      parameter_size_limits['four_byte_max'],      int],
            ['Tm2', int(args.filevalidto),      parameter_size_limits['four_byte_min'],      parameter_size_limits['four_byte_max'],      int],
            ['N',   int(args.nonce),            parameter_size_limits['four_byte_min'],      parameter_size_limits['four_byte_max'],      int]]

        for i in range(0, len(mapping)):
            map(ParameterHandler.mapper(self,
                                        mapping[i][0],
                                        mapping[i][1],
                                        mapping[i][2],
                                        mapping[i][3],
                                        mapping[i][4]), mapping[i])

        self.parameters['Pad_FH1'] = 0
        self.parameters['Pad_FH3'] = 0

        if args.output is None:
            args.output = ''
        self.parameters['Out_Path'], self.parameters['Out_Name'] = os.path.split(args.output)

        return self.parameters

    def mapper(self, param, arg, size_min, size_max, method):
        """Maps the arguments to the dictionary of parameters needed with size limits"""
        if method(arg) < size_min or method(arg) > size_max:
            sys.exit("{} argument is invalid".format(param))
        self.parameters[param] = arg
        return
