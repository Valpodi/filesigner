import unittest
from .buffer_signer import BufferSigner
from .parameter_handler import ParameterHandler


class DefaultExpected:
    first_sha = b'\xa0\xb0\x1a\xddxf\xdf\xf8\n\t\xe9\x05\xc0\x19\xa3\xd4\x88\x13\xf8\xc2\xb8\xcd\xf4< 8\xe6\xaf\xce\\zw'
    second_sha = b'c\xd5\x08o\xec\xd2\xf5kML\xcd[i*\x97\x9f^3\xc4E\x8b\xcbb\xa6\xa6W\x95\xadu\x1f\x1bJ'
    FH1 = b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
          b'\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
          b'\x00\x00\x00\x00'
    FH2 = b'c\xd5\x08o\xec\xd2\xf5kML\xcd[i*\x97\x9f^3\xc4E\x8b\xcbb\xa6\xa6W\x95\xadu\x1f\x1bJ'
    FH3 = b'\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
          b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    contents = b'{rYamlisgreat}'
    default_parameters = {'J': 'testfile.txt',
                          'K': 454086624460063511464984254936031011189294057512315937409637584344757371137,
                          'R': 17,
                          'V': 1,
                          'S': 0,
                          'F': 0,
                          'Ts1': 0,
                          'Ts2': (2**32)-1,
                          'Tm1': 0,
                          'Tm2': (2**32)-1,
                          'N': 1,
                          'Pad_FH1': 0,
                          'Pad_FH3': 0,
                          'Out_Name': ''}


class TestBufferSigner(unittest.TestCase):

    def test_buffer_signer_default(self):
        signed_buffer = BufferSigner().sign_the_buffer(DefaultExpected.default_parameters, DefaultExpected.contents)

        self.assertEqual(signed_buffer[0:96], DefaultExpected.FH1)
        self.assertEqual(signed_buffer[96:128], DefaultExpected.FH2)
        self.assertEqual(signed_buffer[128:160], DefaultExpected.FH3)
        self.assertEqual(signed_buffer[160:], DefaultExpected.contents)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestBufferSigner)
    unittest.TextTestRunner(verbosity=5).run(SUITE)
