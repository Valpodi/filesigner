"""Signs a file to be passed to an OAKDOOR as per the Firmware Specification"""
import sys
import os
from .generate_signing_header import GenerateSigningHeader


def read_file(path, filename):
    """Reads the contents of the target file to be signed"""
    with open(os.path.join(path, filename), "rb") as file_for_signing:
        contents = file_for_signing.read()
    file_for_signing.close()
    return contents


def write_header_to_output_file(header, path, filename, data):
    """
    Writes the header and contents of the file into as a signed file
    into the 'signed' directory with the same name as the target
    """
    with open(os.path.join(path, filename), "wb") as signed_file:
        signed_file.write(header + data)
    signed_file.close()


def sign_the_file(parameters):
    """Trigger the processes to sign a file"""
    file_contents = read_file(parameters['In_Path'], parameters['J'])
    header = GenerateSigningHeader(parameters).execute(file_contents)

    if parameters['Out_Name'] is '':
        write_header_to_output_file(header,
                                    'signed/',
                                    parameters['J'],
                                    file_contents)
    else:
        write_header_to_output_file(header,
                                    parameters['Out_Path'],
                                    parameters['Out_Name'],
                                    file_contents)


if __name__ == '__main__':
    print("please run through package interface", file=sys.stderr)
