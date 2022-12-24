""" Built-in modules """
import re
import sys
from pathlib import Path
# Custom modules #
from Modules.utils import error_query, print_err


# Pseudo-constants #
CHUNK_SIZE = 4096


def main():
    """
    Iterates through input binary, matching words, and creating wordlist from results.

    :return:  Nothing
    """
    ret = 0
    # Get the working directory #
    path = Path('.')

    # If a file name arg was passed in #
    if len(sys.argv) > 1:
        filename = path / sys.argv[1]

        # If the arg file name does not exist #
        if not filename.exists():
            print_err('Passed in arg file name does not exist')
            sys.exit(1)
    # If user failed to provide input file name #
    else:
        print_err('No name of binary file to be parsed provided .. try '
                  'again with \"bin_parser.py <binary_name>\"')
        sys.exit(1)

    string_set = set()
    re_string = re.compile(b'[a-zA-Z0-9!@$&(-_"\'.,]{4,15}(?: |$)')

    mode = 'rb'
    try:
        with filename.open(mode) as bin_file:
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

        filename = path / 'wordlist.txt'
        mode = 'a'
        # Write result wordlist #
        with filename.open(mode, encoding='utf-8') as out_file:
            for string in string_set:
                out_file.write(f'{string}\n')

    # If error occurs during file operation #
    except (IOError, OSError) as file_err:
        # Look up specific error with errno module #
        error_query(str(filename.resolve()), mode, file_err)
        ret = 2

    sys.exit(ret)


if __name__ == '__main__':
    main()
