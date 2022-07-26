# Built-in modules #
import re
import sys

# Custom modules #
from Modules.Utils import ErrorQuery, PrintErr


"""
########################################################################################################################
Name:       main
Purpose:    Iterates through input file, matching words, and creating wordlist from results.
Parameters: None
Returns:    None
########################################################################################################################
"""
def main():
    # If a file name arg was passed in #
    if len(sys.argv) > 1:
        filename = f'./{sys.argv[1]}'
    else:
        PrintErr('No name of file to be parsed provided as arg .. try again with \"Text_Parser.py <file name>\"')
        sys.exit(1)

    # Only record unique strings #
    string_set = set()
    # Compile string matching regex #
    re_string = re.compile(r'[a-zA-Z]{3,15}(?: |$)')

    try:
        with open(filename, 'r') as file:
            for line in file:
                # Check line of text for matches, populate into list #
                string_parse = re.findall(re_string, line)

                # If regex matches #
                if string_parse:
                    # Filter out phrases with minimal value #
                    parse_tuple = ('True', 'False')
                    string_parse = [string.strip() for string in string_parse if string not in parse_tuple]

                    # Write results to report file #
                    [string_set.add(string) for string in string_parse]

    # If file error occurs #
    except (IOError, OSError) as err:
        ErrorQuery(filename, 'r', err)

    try:
        # Open the wordlist in append mode #
        with open('wordlist.txt', 'a') as report_file:
            for string in string_set:
                # Remove extra whitespace #
                parse = string.strip()
                # Write result to report file #
                report_file.write(f'{parse}\n')

    # If file error occurs #
    except (IOError, OSError) as err:
        ErrorQuery('wordlist.txt', 'a', err)

    sys.exit(0)


if __name__ == '__main__':
    main()
