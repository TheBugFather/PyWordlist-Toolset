# Built-in modules #
import os
import re
import sys

# Custom modules #
from Modules.Utils import ErrorQuery, PrintErr


"""
########################################################################################################################
Name:       main
Purpose:    Iterates through input file, matching words, and creating wordlist from results.
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
        PrintErr('No name of file to be parsed provided .. try again with \"WordlistFileParser.py <file name>\"')
        sys.exit(1)

    # Only record unique strings #
    string_set = set()
    # Compile string matching regex #
    re_string = re.compile(r'[a-zA-Z\d!@$&(\-_\"\'.,]{4,15}(?: |$)')

    mode = 'r'
    try:
        with open(filename, mode) as file:
            for line in file:
                # Check line of text for matches, populate into list #
                string_parse = re.findall(re_string, line)

                # If regex matches #
                if string_parse:
                    # Tuple for specifying which words to filter out #
                    parse_tuple = ('True', 'False')
                    # Filter out phrases with minimal value #
                    string_parse = [string.strip() for string in string_parse if string not in parse_tuple]
                    # Write results to report file #
                    [string_set.add(string) for string in string_parse]

        filename = 'wordlist.txt'
        mode = 'a'
        # Open the wordlist in append mode #
        with open(filename, mode) as report_file:
            # Iterate through each string in unique set #
            for string in string_set:
                # Remove extra whitespace #
                parse = string.strip()
                # Write result to report file #
                report_file.write(f'{parse}\n')

    # If error occurs during file operation #
    except (IOError, OSError) as file_err:
        # Look up specific error with errno module #
        ErrorQuery(filename, mode, file_err)
        sys.exit(2)

    sys.exit(0)


if __name__ == '__main__':
    main()
