# Built-in modules #
import os
import sys

# External modules #
import requests
from bs4 import BeautifulSoup

# Custom modules #
from Modules.Utils import ErrorQuery, PrintErr


"""
########################################################################################################################
Name:       main
Purpose:    Iterates through input url file, scraping text data, and writing results as wordlist.
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
        PrintErr('No name of file to be parsed provided .. try again with \"ScrapeParser.py <url list>\"')
        sys.exit(1)

    scrape_set = set()
    print(f'Scraping text from url list to create custom wordlist\n{"*" * 54}\n')

    mode = 'r'
    try:
        with open(filename, mode) as in_file:
            # Iterate through url list line by line #
            for line in in_file:
                print(line)
                # Use a get request to fetch webpage contents #
                get_page = requests.get(line)
                # Initialize Beautiful Soup web parser #
                soup = BeautifulSoup(get_page.text, 'html.parser')
                # Get the page text data #
                page_text = soup.get_text()

                # Iterate through scraped text line by line #
                for string_line in page_text.split('\n'):
                    # Iterate through each word in line #
                    for string in string_line:
                        # Add unique strings to set #
                        scrape_set.add(string)

        filename = 'wordlist.txt'
        mode = 'a'
        # Write the result set to output wordlist #
        with open(filename, mode) as out_file:
            for string in scrape_set:
                out_file.write(f'{string}\n')

    # If error occurs during file operation #
    except (IOError, OSError) as file_err:
        PrintErr(f'Error occurred during file operation: {file_err}')
        ErrorQuery(filename, mode, file_err)
        sys.exit(2)

    sys.exit(0)


if __name__ == '__main__':
    main()
