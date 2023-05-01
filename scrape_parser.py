# pylint: disable=W0106
""" Built-in modules """
import re
import sys
from pathlib import Path
# External modules #
import requests
from bs4 import BeautifulSoup
# Custom modules #
from Modules.utils import error_query, print_err


# Target IP or domain name #
TARGET = '<Add IP or Domain>'
# Specify whether http or https #
PROTO = '<Add http or https>'


def get_webpage(web_page: str):
    """
    Uses beautiful soup to retrieve web page text data.

    :param web_page:  The web page to be retrieved.
    :return:  The scraped web page data.
    """
    # Use a get request to fetch webpage contents #
    get_page = requests.get(web_page)
    # Initialize Beautiful Soup web parser #
    soup = BeautifulSoup(get_page.text, 'html.parser')
    # Get the page text data #
    return soup.get_text()


def arg_check(file_path: Path) -> Path:
    """
    Checks if user passed in filename arg, raises error if no arg was passed in. If the file name \
    arg passed in does not exist an error is raised to inform the user of their improper input.

    :param file_path:  Path to the input file name.
    :return:  File name on success, exit code 1 on failure.
    """
    # If a file name arg was passed in #
    if len(sys.argv) > 1:
        filename = file_path / sys.argv[1]

        # If the arg file name does not exist #
        if not filename.exists():
            print_err('Passed in arg file name does not exist')
            sys.exit(1)
    # If user failed to provide input file name #
    else:
        print_err('No name of file to be parsed provided .. try'
                  ' again with \"scrape_parser.py <url_list>\"')
        sys.exit(1)

    return filename


def main():
    """
    Iterates through input url file, scraping text data, and writing results as wordlist.

    :return:  Nothing
    """
    ret = 0
    # Get the working directory #
    path = Path.cwd()
    # Check to see if user passed in file name #
    filename = arg_check(path)

    scrape_set = set()
    re_parse = re.compile(r'^/[a-zA-Z\d.-]{1,255}')
    re_string = re.compile(r'[a-zA-Z\d!@$&(\-_\"\'.,]{4,15}(?: |$)')

    print(f'\nScraping text from url list to create custom wordlist\n{"*" * 54}\n')

    mode = 'r'
    try:
        with filename.open(mode, encoding='utf-8') as in_file:
            # Iterate through url list line by line #
            for line in in_file:
                print(line)

                # Search the line for the web path #
                ext_path = re.search(re_parse, line)
                # If the regex to grab web path failed #
                if not ext_path:
                    continue

                # If the protocol is HTTP #
                if PROTO == 'http':
                    request = f'http://{TARGET}{ext_path.group(0)}'
                # If the protocol is HTTPS #
                elif PROTO == 'https':
                    request = f'https://{TARGET}{ext_path.group(0)}'
                # If improper protocol was specified #
                else:
                    print_err('Improper protocol specified, put either http '
                             'or https in PROTO variable in program header')
                    sys.exit(2)

                # Get the page text data #
                page_text = get_webpage(request)

                # Match all strings in the page text #
                strings = re.findall(re_string, page_text)

                # If the page has word strings #
                if strings:
                    # Write the result strings to string set #
                    [scrape_set.add(string) for string in strings]

        filename = path / 'wordlist.txt'
        mode = 'a'
        # Write the result set to output wordlist #
        with filename.open(mode, encoding='utf-8') as out_file:
            for string in scrape_set:
                out_file.write(f'{string}\n')

    # If error occurs during file operation #
    except OSError as file_err:
        # Look up specific error with errno module #
        error_query(str(filename), mode, file_err)
        ret = 3

    sys.exit(ret)


if __name__ == '__main__':
    main()
