# Built-in modules #
import os
import sys

# Custom modules #
from Modules.Utils import ErrorQuery, PrintErr


"""
########################################################################################################################
Name:       main
Purpose:    Iterates through input wordlist, stripping any extra whitespace outside of each item and overwriting the \
            results to a fresh sanitized wordlist.
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
    # If user failed to provide input wordlist name #
    else:
        PrintErr('No name of wordlist file provided .. try again with \"WordlistSanitizer <wordlist name>\"')
        sys.exit(1)

    # Filter set with only unique strings #
    parse_set = set()

    mode = 'r'
    try:
        # Open current wordlist in read mode #
        with open(filename, mode) as file:
            for line in file:
                # Strip out unnecessary whitespace #
                parsed_text = line.strip()
                # Add parsed text to set #
                parse_set.add(parsed_text)

        mode = 'w'
        # Overwrite the old word list #
        with open(filename, mode) as report_file:
            # Write result wordlist #
            for parse in parse_set:
                report_file.write(f'{parse}\n')

    # If error occurs during file operation #
    except (IOError, OSError) as file_err:
        PrintErr(f'Error occurred during wordlist sanitation: {file_err}')
        ErrorQuery(filename, mode, file_err)
        sys.exit(2)

    sys.exit(0)


if __name__ == '__main__':
    main()
