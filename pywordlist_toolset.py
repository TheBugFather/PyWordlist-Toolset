# pylint: disable=W0106
""" Built-in modules """
import argparse
import logging
import re
import sys
from pathlib import Path
# External modules #
import requests
from bs4 import BeautifulSoup
# Custom modules #
from Modules.utils import error_query, print_err, wordlist_writer


# Specify fluff words to filter from wordlist #
PARSE_TUPLE = ('True', 'False', 'true', 'false')


def get_webpage(config_obj: object, parsed_request: str) -> str | bool:
    """
    Perform a get request on target webpage and return the scrape data in text format.

    :param config_obj:  The program configuration instance.
    :param parsed_request:  The request data parsed from specified source file.
    :return:  Returns scrape web data as text on success, False boolean on failure.
    """
    # If the request is missing the protocol #
    if not parsed_request.startswith('http'):
        parsed_request = f'http://{config_obj.host}:{config_obj.port}{parsed_request}'

    while True:
        # Use a get request to fetch webpage contents #
        get_page = requests.get(parsed_request)
        # If the initial HTTP request fails #
        if get_page.status_code != 200 and not parsed_request.startswith('https'):
            # Reformat the request as HTTPS and try again #
            parsed_request = f'https://{parsed_request.split("//")[1]}'
            continue

        # If the second HTTPS request fails #
        if get_page.status_code != 200 and parsed_request.startswith('https'):
            return False

        break

    # Initialize Beautiful Soup web parser #
    soup = BeautifulSoup(get_page.text, 'html.parser')
    # Get the page text data #
    return soup.get_text()


def scrape_handler(config_obj: object):
    """
    Handles reading urls from source file, performing regex to determine source data format, and
    passing necessary resources into the get_webpage() call to retrieve the web page data. Once the
    web page data has been gathered the words in the text data are matched with regex and written
    to the output wordlist.

    :param config_obj:  The program configuration instance.
    :return:  Nothing
    """
    try:
        # Open the source file passed in as arg for parsing #
        with config_obj.in_file.open('r', encoding='utf-8') as in_file:
            # Iterate through url list line by line #
            for line in in_file:
                print(line)

                # If the wordlist scrape mode was selected #
                if config_obj.mode == 'scrape':
                    ext_path = re.search(config_obj.re_gobuster_parse, line)
                # If Gobuster scrape mode was selected #
                else:
                    # Search the line for the web path #
                    ext_path = re.search(config_obj.re_text_word, line)

                # If all web scraping regex patterns fail, skip current line #
                if not ext_path:
                    continue

                # Get the web page text data #
                page_text = get_webpage(config_obj, ext_path.group(0))
                # If the retrieval of web page text data fails #
                if not page_text:
                    continue

                # Match all strings in the page text #
                strings = re.findall(config_obj.re_text_word, page_text)
                # If the page has word strings #
                if strings:
                    # Add string data to string set to filter duplicates #
                    [config_obj.parse_set.add(string) for string in strings
                     if string not in config_obj.parse_tuple]

    # If error occurs during file operation #
    except OSError as file_err:
        # Look up specific error with errno module #
        error_query(str(config_obj.in_file), 'r', file_err)

    # Write the parsed web data as wordlist #
    wordlist_writer(config_obj, config_obj.out_file, 'a')


def sanitize_handler(config_obj: object):
    """
    Handles reading input wordlist, performs sanitation to ensure clean formatting, and writes the
    result to output wordlist.

    :param config_obj:  The program configuration instance.
    :return:  Nothing
    """
    # Create filter tuple with punctuation and quotes #
    punc = (',', '.', ':', ';', '\'', '"')

    try:
        # Open current wordlist in read mode #
        with config_obj.in_file.open('r', encoding='utf-8') as file:
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

                # Strip out unnecessary whitespace #
                parsed_text.strip()
                # Add parsed text to set #
                config_obj.parse_set.add(parsed_text)

    # If error occurs during file operation #
    except OSError as file_err:
        # Look up specific error with errno module #
        error_query(str(config_obj.in_file), 'r', file_err)

    # Overwrite the passed in wordlist with sanitized result #
    wordlist_writer(config_obj, config_obj.in_file, 'w')


def text_handler(config_obj: object):
    """
    Handles reading data from input text file, matching words with regex, and writing parsed words
    to output wordlist.

    :param config_obj: The program configuration instance.
    :return:  Nothing
    """
    try:
        # Open source text file and read string data #
        with config_obj.in_file.open('r', encoding='utf-8') as text_file:
            for line in text_file:
                # Check line of text for matches, populate into list #
                string_parse = re.findall(config_obj.re_text_word, line)
                # If regex matches #
                if string_parse:
                    # Filter out phrases with minimal value and strip extra whitespace #
                    string_parse = [string.strip() for string in string_parse
                                    if string not in config_obj.parse_tuple]
                    # Write results to report file #
                    [config_obj.parse_set.add(string) for string in string_parse]

    # If error occurs during file operation #
    except OSError as file_err:
        # Look up specific error with errno module #
        error_query(str(config_obj.in_file), 'r', file_err)

    # Write the parsed text data as wordlist #
    wordlist_writer(config_obj, config_obj.out_file, 'a')


def bin_handler(conf_obj: object):
    """
    Reads binary file chunk by chunk, parses out words, and formats parsed words into the output
    wordlist file.

    :param conf_obj:  The program configuration instance.
    :return:  Nothing
    """
    try:
        # Open binary source file and ready byte data #
        with conf_obj.in_file.open('rb') as bin_file:
            while True:
                # Ready a chunk from the source file #
                chunk = bin_file.read(4096)
                # If no chunk of data because EOF #
                if not chunk:
                    break

                # Find all regex matches formatted as a list #
                string_parse = re.findall(conf_obj.re_bin_word, chunk)
                # If regex match was successful #
                if string_parse:
                    # Append unique words to match set #
                    [conf_obj.parse_set.add(string.decode().strip()) for string in string_parse
                     if string.decode() not in conf_obj.parse_tuple]

    # If error occurs during file operation #
    except OSError as file_err:
        # Look up specific error with errno module #
        error_query(str(conf_obj.in_file), 'rb', file_err)

    # Write the parsed and decoded binary word data as wordlist #
    wordlist_writer(conf_obj, conf_obj.out_file, 'a')


class ProgramConfig:
    """
    Program configuration class for storing program components.
    """
    def __init__(self):
        # Program variables #
        self.cwd = Path.cwd()
        self.in_file = None
        self.out_file = self.cwd / 'PyWordlist.txt'
        self.mode = None
        self.host = None
        self.port = None
        self.parse_set = set()
        self.parse_tuple = PARSE_TUPLE

        # Program compiled regex patterns #
        self.re_ipv4 = re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
        self.re_ipv6 = re.compile(r'^([0-9a-f]{0,4}:){2,7}(:|[0-9a-f]{1,4})$')
        self.re_domain = re.compile(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+'
                                    r'[a-zA-Z]{2,6}$')
        self.re_bin_word = re.compile(b'[a-zA-Z0-9!@$&(-_\"\'.,]{4,15}(?: |$)')
        self.re_text_word = re.compile(r'[a-zA-Z\d!@$&(\-_\"\'.,]{4,15}(?: |$)')
        self.re_gobuster_parse = re.compile(r'^/[a-zA-Z\d.-]{1,255}')

    def parse_in_file(self, file_path: str):
        """
        Ensure passed in command line arg points to a valid file that exist.

        :param file_path:  The path to file to ensure exists before storing in program config.
        :return:  Nothing
        """
        # Format passed in string as path #
        test_path = Path(file_path)
        # If the passed in file path does not exist #
        if not test_path.exists():
            # Print error, log, and exit with error code #
            print_err(f'Passed in file path of {test_path.name} does not exist')
            logging.error('Passed in file path of %s does not exist', test_path.name)
            sys.exit(2)

        self.in_file = test_path

    def parse_host(self, host: str):
        """
        Ensure passed in command line arg is of proper IPv4/6 or domain format before storing in
        program config.

        :param host:  The host to be validated and stored in program config.
        :return:  Nothing
        """
        # Check host arg with IP4/6 and domain regex patterns #
        ipv4_match = re.search(self.re_ipv4, host)
        ipv6_match = re.search(self.re_ipv6, host)
        domain_match = re.search(self.re_domain, host)

        # If the arg matches none of the required formats #
        if not ipv4_match and not ipv6_match and not domain_match:
            # Print error, log, and exit with error code #
            print_err(f'Passed in host argument {host} does not match IPv4/6 or domain format')
            logging.error('Passed in host argument %s does not match IPv4/6 or domain format', host)
            sys.exit(2)

        # If host is IPv6 format #
        if ipv6_match:
            # Add external brackets to prevent request errors #
            host = f'[{host}]'

        self.host = host

    def parse_port(self, port: int):
        """
        Ensure passed in command line arg is of proper integer port range before storing in program
        config.

        :param port:  The integer port number to connect to remote web server.
        :return:  Nothing
        """
        # If port is out of expected range #
        if port > 80 or port < 65535:
            # Print error, log, and exit with error code #
            print_err(f'Passed in port {port} is out of expected port range of 80-65535')
            logging.error('Passed in port %s is out of expected port range of 80-65535', port)
            sys.exit(2)

        self.port = port


def main():
    """
    Initializes program configuration, parses command line arguments, validates then stores args in
    program configuration class, and performs operation based on specified mode.

    :return:  Nothing
    """
    print(r'''
     _____    __          __           _ _ _     _     _______          _          _   
    |  __ \   \ \        / /          | | (_)   | |   |__   __|        | |        | |  
    | |__) |   \ \  /\  / /__  _ __ __| | |_ ___| |_     | | ___   ___ | |___  ___| |_ 
    |  ___/ | | \ \/  \/ / _ \| '__/ _` | | / __| __|    | |/ _ \ / _ \| / __|/ _ \ __|
    | |   | |_| |\  /\  / (_) | | | (_| | | \__ \ |_     | | (_) | (_) | \__ \  __/ |_ 
    |_|    \__, | \/  \/ \___/|_|  \__,_|_|_|___/\__|    |_|\___/ \___/|_|___/\___|\__|
            __/ |                                                                      
           |___/                                                                       
    ''')
    # Initialize the program configuration class #
    config_obj = ProgramConfig()

    # Parse command line arguments #
    arg_parser = argparse.ArgumentParser(description='The Python wordlist generation toolset')
    arg_parser.add_argument('file_path', help='Path to the file to be parsed into in a wordlist or '
                                              'the wordlist file for scraping operations')
    arg_parser.add_argument('mode', choices=['bin', 'text', 'sanitize', 'scrape', 'gobuster'],
                            help='Sets execution mode, supported modes: (bin, text, sanitize,'
                                 ' scrape, gobuster)')
    arg_parser.add_argument('--host', help='Remote host to scrape web data into wordlist, supports'
                                           ' IPv4, IPv6, and domain format')
    arg_parser.add_argument('--port', type=int, help='TCP port to connect on remote host to'
                                                     ' access webpage for scraping data')
    args = arg_parser.parse_args()

    # Parse and validate the args into the configuration class #
    config_obj.parse_in_file(args.file_path)
    # If optional args were passed in, parse them into config class #
    if args.host:
        config_obj.parse_host(args.host)
    if args.port:
        config_obj.parse_port(args.port)

    # Make sure host and port are specified for web scraping related modes #
    if (args.mode in ('scrape', 'gobuster')) and (not args.host or not args.port):
        # Print error, log, and exit with error code #
        print_err('Specified mode that requires host and port but at least one is missing')
        logging.error('Specified mode that requires host and port but at least one is missing')
        sys.exit(2)

    config_obj.mode = args.mode

    # If the binary file mode was selected #
    if config_obj.mode == 'bin':
        bin_handler(config_obj)
    # If the text file mode was selected #
    elif config_obj.mode == 'text':
        text_handler(config_obj)
    # If the sanitizer mode was selected #
    elif config_obj.mode == 'sanitize':
        sanitize_handler(config_obj)
    # If the scrape mode was selected #
    elif config_obj.mode == 'scrape':
        scrape_handler(config_obj)
    # If the gobuster scrape mode was selected #
    else:
        scrape_handler(config_obj)


if __name__ == '__main__':
    ret = 0
    # Setup the log file and logging facilities #
    logging.basicConfig(filename='pyWordlist-Toolset.log',
                        format='%(asctime)s %(lineno)4d@%(filename)-22s[%(levelname)s]>>  '
                               ' %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    try:
        main()

    # If unknown exception occurs #
    except Exception as err:
        # Print error, log, and set error exit code #
        print_err(f'Unexpected error occurred: {err}')
        logging.exception('Unexpected error occurred: %s', err)
        ret = 1

    sys.exit(ret)
