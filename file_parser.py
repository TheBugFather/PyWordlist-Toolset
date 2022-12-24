# pylint: disable=W0106
""" Built-in modules """
import re
import sys
from pathlib import Path
# Custom modules #
from Modules.utils import error_query, print_err


def main():
    """
    Iterates through input file, matching words, and creating wordlist from results.

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
        print_err('No name of file to be parsed provided .. try '
                  'again with \"file_parser.py <file_name>\"')
        sys.exit(1)

    # Only record unique strings #
    string_set = set()
    # Compile string matching regex #
    re_string = re.compile(r'[a-zA-Z\d!@$&(\-_\"\'.,]{4,15}(?: |$)')

    mode = 'r'
    try:
        with filename.open(mode, encoding='utf-8') as file:
            for line in file:
                # Check line of text for matches, populate into list #
                string_parse = re.findall(re_string, line)

                # If regex matches #
                if string_parse:
                    # Tuple for specifying which words to filter out #
                    parse_tuple = ('True', 'False')
                    # Filter out phrases with minimal value and strip extra whitespace #
                    string_parse = [string.strip() for string in string_parse
                                    if string not in parse_tuple]
                    # Write results to report file #
                    [string_set.add(string) for string in string_parse]

        filename = path / 'wordlist.txt'
        mode = 'a'
        # Open the wordlist in append mode #
        with filename.open(mode, encoding='utf-8') as report_file:
            # Iterate through each string in unique set #
            for string in string_set:
                # Remove extra whitespace #
                parse = string.strip()
                # Write result to report file #
                report_file.write(f'{parse}\n')

    # If error occurs during file operation #
    except (IOError, OSError) as file_err:
        # Look up specific error with errno module #
        error_query(str(filename.resolve()), mode, file_err)
        ret = 2

    sys.exit(ret)


if __name__ == '__main__':
    main()
