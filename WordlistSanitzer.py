# Built-in modules #
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
        PrintErr('No name of wordlist file provided .. try again')
        sys.exit(1)

    # Filter set with only unique strings #
    parse_set = set()

    try:
        # Open current wordlist in read mode #
        with open(filename, 'r') as file:
            for line in file:
                # Strip out unnecessary whitespace #
                parsed_text = line.strip()
                # Add parsed text to set #
                parse_set.add(parsed_text)

    # If file error occurs #
    except (IOError, OSError) as err:
        ErrorQuery(filename, 'r', err)

    try:
        # Overwrite the old word list #
        with open(filename, 'w') as report_file:
            # Write result to report file #
            [report_file.write(f'{parse}\n') for parse in parse_set]

    # If file error occurs #
    except (IOError, OSError) as err:
        ErrorQuery(filename, 'w', err)

    sys.exit(0)


if __name__ == '__main__':
    main()
