# filesigner
## Purpose
To sign a file prior to export through an Oakdoor Export Diode™ or Oakdoor Gateway™.

This repository contains source code and python scripts for the filesigner program. 

## Prerequisites
* Python3 installed
* Python dependencies, install using: 


    pip3 install -r filesigner/requirements.txt

## How to Use
* Pull/Download the repository
* Check the help
* Sign an example file

### Pull/Download the repository

    git clone git@github.com:oakdoor/filesigner.git

You should see a folder called filesigner with mostly .py files within it.    

### Check you can call the package and see the help
From the filesigner directory, run:

    python3 -m filesigner -h
    
This should show the help for the filesigner.

### Sign an example file
The following command signs a file:

    python3 -m filesigner -J [FILENAME]
    
Note that the filesigner needs a "signed" directory on the same level when signing files. 
For example:

    main_directory
    └── filesigner
        ├── README.md
        ├── module1.py
        ├── module2.py 
        ├── ... 
        └── example_file.txt
    └── signed
    
To then sign the example_file.txt, run:
    
    python3 -m filesigner -J filesigner/example_file.txt
    
This should create a new file in the "signed" directory with the same name (example_file.txt) and with a signature header. 

## Additional Detail
If no filename is given using -J then the filesigner looks for a file called "testfile.txt" in the main directory. 

All other input arguments relate to the signing parameters. Default values can be found in the parameter_handler.py file.

For a more detailed description of filesigner inputs, see below:

    python3 -m filesigner -h:
    usage: python3 -m filesigner [-h] [-J FILENAME] [-K UNIQUEID] [-R REGTOKEN]
                          [-V VERSION] [-S SIZE] [-F FORMAT]
                          [-Ts1 SESSIONVALIDFROM] [-Ts2 SESSIONVALIDTO]
                          [-Tm1 FILEVALIDFROM] [-Tm2 FILEVALIDTO] [-N NONCE]

    Sign a file using the 'Release Control' process

    optional arguments:
      -h, --help            show this help message and exit
      -J FILENAME, --filename FILENAME
                            Specify the file to be signed
      -K UNIQUEID, --uniqueid UNIQUEID
                            Specify the shared unique id <hex number, max size 32
                            bytes>
      -R REGTOKEN, --regtoken REGTOKEN
                            Specify the registration token <hex number, max size
                            32 bytes>
      -V VERSION, --version VERSION
                            Specify the 'Release Control' version <int>
      -S SIZE, --size SIZE  Specify the maximum file size <bytes>
      -F FORMAT, --format FORMAT
                            Specify the file format allowed to egress <0 for all,
                            1 for rYAML, 2 for BMP>
      -Ts1 SESSIONVALIDFROM, --sessionvalidfrom SESSIONVALIDFROM
                            Specify the Session ID 'validfrom' time <unix uint32>
      -Ts2 SESSIONVALIDTO, --sessionvalidto SESSIONVALIDTO
                            Specify the Session ID 'validto' time <unix uint32>
      -Tm1 FILEVALIDFROM, --filevalidfrom FILEVALIDFROM
                            Specify the signed file 'valid from' time <unix
                            uint32>
      -Tm2 FILEVALIDTO, --filevalidto FILEVALIDTO
                            Specify the signed file 'valid to' time <unix uint32>
      -N NONCE, --nonce NONCE
                            Specify the nonce for the file <int>



    Argument Defaults:
        J       'testfile.txt'
        K       '01' repeating              <hexadecimal 32 byte word>
        R       '11'                        <hexadecimal 32 byte word>
        V       '1'                         <decimal 4 byte word>
        S       '0'                         <decimal 4 byte word>
        F       '0'                         <decimal 4 byte word>
        Ts1     '0'                         <unix uint32 epoch min>
        Ts2     '4294967295'                <unix uint32 epoch max>
        Tm1     '0'                         <unix uint32 epoch min>
        Tm2     '4294967295'                <unix uint32 epoch max>
        N       '1'                         <decimal 4 byte word>
        _unwrapped_file.txt" which should be identical to "example_unwrapped_file.txt"
