"""Generates a header to sign a file"""
import hashlib
import construct


class GenerateSigningHeader(object):
    """Creates hashes from given parameters and constructs the header needed for a signed file"""
    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, data):
        """Trigger the methods required to make the header for the signed file"""
        kr = self.calculate_kr()
        h = self.calculate_h(kr, data)
        return self.make_header(h)

    def calculate_kr(self):
        """Calculates the Kr hash as per the OAKDOOR Firmware Specification"""
        kr_parameters = construct.Struct(
            "V" / construct.Int32ub,
            "R" / construct.BytesInteger(32),
            "S" / construct.Int32ub,
            "F" / construct.Int32ub,
            "Ts1" / construct.Int32ub,
            "Ts2" / construct.Int32ub,
            "Pad_FH1" / construct.BytesInteger(44),
            "K" / construct.BytesInteger(32))

        bytestring = kr_parameters.build(dict(V=self.parameters['V'],
                                              R=self.parameters['R'],
                                              S=self.parameters['S'],
                                              F=self.parameters['F'],
                                              Ts1=self.parameters['Ts1'],
                                              Ts2=self.parameters['Ts2'],
                                              Pad_FH1=self.parameters['Pad_FH1'],
                                              K=self.parameters['K']))

        return self.calculate_hash(bytestring)

    @staticmethod
    def calculate_hash(bytestring):
        """Generates a sha256 hash for a given byte array"""
        sha256_hash = hashlib.new('SHA256')
        sha256_hash.update(bytestring)
        print("The hash is: {}".format(sha256_hash.hexdigest()))

        return  sha256_hash.digest()

    def calculate_h(self, Kr, X):
        """Calculates the H hash as per the OAKDOOR Firmware Specification"""
        h_parameters = construct.Struct(
            "N" / construct.Int32ub,
            "J" / construct.GreedyString('utf8'), #'GreedyString' reads until the end of stream
            "Tm1" / construct.Int32ub,
            "Tm2" / construct.Int32ub)

        bytestring = X + h_parameters.build(dict(N=self.parameters['N'],
                                                 J=self.parameters['J'],
                                                 Tm1=self.parameters['Tm1'],
                                                 Tm2=self.parameters['Tm2'])) + Kr

        return self.calculate_hash(bytestring)

    def make_header(self, H):
        """
        Creates the header from the given parameters
        and associated hash that are required to sign a file
        """
        fh1_constructor = construct.Struct(
            "V" / construct.Int32ub,
            "R" / construct.BytesInteger(32),
            "S" / construct.Int32ub,
            "F" / construct.Int32ub,
            "Ts1" / construct.Int32ub,
            "Ts2" / construct.Int32ub,
            "Pad_FH1" / construct.BytesInteger(44))

        FH1 = fh1_constructor.build(dict(V=self.parameters['V'],
                                         R=self.parameters['R'],
                                         S=self.parameters['S'],
                                         F=self.parameters['F'],
                                         Ts1=self.parameters['Ts1'],
                                         Ts2=self.parameters['Ts2'],
                                         Pad_FH1=self.parameters['Pad_FH1']))

        fh3_constructor = construct.Struct(
            "Tm1" / construct.Int32ub,
            "Tm2" / construct.Int32ub,
            "N" / construct.Int32ub,
            "Pad_FH3" / construct.BytesInteger(20))

        FH3 = fh3_constructor.build(dict(Tm1=self.parameters['Tm1'],
                                         Tm2=self.parameters['Tm2'],
                                         N=self.parameters['N'],
                                         Pad_FH3=self.parameters['Pad_FH3']))

        FH2 = H

        print("FH1 is: {}".format(FH1))
        print("FH2 is: {}".format(FH2))
        print("FH3 is: {}".format(FH3))

        return FH1 + FH2 + FH3
