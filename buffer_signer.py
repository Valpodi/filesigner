"""Signs a file to be passed to an OAKDOOR as per the Firmware Specification"""
from .generate_signing_header import GenerateSigningHeader


class BufferSigner(object):
    @staticmethod
    def sign_the_buffer(parameters, buffer):
        """Trigger the processes to sign a buffer"""
        return GenerateSigningHeader(parameters).execute(buffer) + buffer
