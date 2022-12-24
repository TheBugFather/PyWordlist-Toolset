""" Built-in modules """
import sys
from pathlib import Path
# Custom modules #
from Modules.utils import error_query, print_err


def main():
    """
    Iterates through input wordlist, stripping any extra whitespace outside each item, removing \
    any punctuation or quotation marks from beginning and ending of string, and overwriting the \
    results to a fresh sanitized wordlist.

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
    # If user failed to provide input wordlist name #
    else:
        print_err('No name of wordlist file provided .. try again '
                  'with \"sanitizer.py <wordlist_name>\"')
        sys.exit(1)

    # Filter set with only unique strings #
    parse_set = set()
    # Create filter tuple with punctuation and quotes #
    punc = (',', '.', ':', ';', '\'', '"')

    mode = 'r'
    try:
        # Open current wordlist in read mode #
        with filename.open(mode, encoding='utf-8') as file:
            # Iterate through file line by line #
            for line in file:
                # Strip out unnecessary whitespace #
                parsed_text = line.strip()

                # If the string starts with punctuation or quotes #
                if parsed_text.startswith(punc):
                    # Index slice character from string start #
                    parsed_text = parsed_text[1:]

                # If the string ends with punctuation or quotes #
                if parsed_text.endswith(punc):
                    # Index slice character from string end #
                    parsed_text = parsed_text[:-1]

                # Add parsed text to set #
                parse_set.add(parsed_text)

        mode = 'w'
        # Overwrite the old word list #
        with filename.open(mode, encoding='utf-8') as report_file:
            # Write result wordlist #
            for parse in parse_set:
                report_file.write(f'{parse}\n')

    # If error occurs during file operation #
    except (IOError, OSError) as file_err:
        # Look up specific error with errno module #
        error_query(str(filename.resolve()), mode, file_err)
        ret = 2

    sys.exit(ret)


if __name__ == '__main__':
    main()
