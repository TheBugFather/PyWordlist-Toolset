# Built-in modules #
import os
import re
import sys

# Custom modules #
from Modules.Utils import ErrorQuery, PrintErr


# Pseudo-constants #
CHUNK_SIZE = 4096


"""
########################################################################################################################
Name:       main
Purpose:    Iterates through input binary, matching words, and creating wordlist from results.
Parameters: Nothing
Returns:    Nothing
########################################################################################################################
"""
def main():
    # Get the working directory #
    cwd = os.getcwd()

    # If the OS is Windows #
    if os.name == 'nt':
        path = f'{cwd}\\'
    # If the OS is Linux #
    else:
        path = f'{cwd}/'

    # If a file name arg was passed in #
    if len(sys.argv) > 1:
        filename = f'{path}{sys.argv[1]}'

        # If the arg file name does not exist #
        if not os.path.isfile(filename):
            PrintErr('Passed in arg file name does not exist')
            sys.exit(1)
    # If user failed to provide input file name #
    else:
        PrintErr('No name of file to be parsed provided .. try again with \"WordlistBinParser.py <bin name>\"')
        sys.exit(1)

    string_set = set()
    re_string = re.compile(b'[a-zA-Z\d !@$&(-_"\'.,]{4,15}(?: |$)')

    mode = 'rb'
    try:
        with open(filename, mode) as bin_file:
            while True:
                # Ready a chunk from the
                chunk = bin_file.read(CHUNK_SIZE)

                # If chunk of data was read #
                if chunk:
                    # Find all regex matches formatted as a list #
                    string_parse = re.findall(re_string, chunk)

                    # If regex match was successful #
                    if string_parse:
                        # Append to match list via list comprehension #
                        for string in string_parse:
                            string_set.add(string.decode())

                # If no data chunk #
                else:
                    break

        filename = 'wordlist.txt'
        mode = 'a'
        # Write result wordlist #
        with open(filename, mode) as out_file:
            for string in string_set:
                out_file.write(f'{string}\n')

    # If error occurs during file operation #
    except (IOError, OSError) as err:
        PrintErr(f'Error occurred during file operation: {err}')
        ErrorQuery(filename, mode, err)
        sys.exit(2)

    sys.exit(0)


if __name__ == '__main__':
    main()
