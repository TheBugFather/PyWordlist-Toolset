""" Built-in modules """
import errno
import sys
from pathlib import Path


def error_query(err_path: str, err_mode: str, err_obj):
    """
    Looks up the errno message to get description.

    :param err_path:  The path to the file where the error occurred.
    :param err_mode:  The file mode used during the error.
    :param err_obj:  The error message instance.
    :return:  Nothing
    """
    # If file does not exist #
    if err_obj.errno == errno.ENOENT:
        print_err(f'{err_path} does not exist')

    # If the file does not have read/write access #
    elif err_obj.errno == errno.EPERM:
        print_err(f'{err_path} does not have permissions for {err_mode}'
                  ' file mode, if file exists confirm it is closed')

    # File IO error occurred #
    elif err_obj.errno == errno.EIO:
        print_err(f'IO error occurred during {err_mode} mode on {err_path}')

    # If other unexpected file operation occurs #
    else:
        print_err(f'Unexpected file operation occurred accessing {err_path}: {err_obj.errno}')


def print_err(msg: str):
    """
    Prints error message through standard error.

    :param msg:  The error message to be displayed.
    :return:  Nothing
    """
    #  Print error via standard error #
    print(f'\n* [ERROR] {msg} *\n', file=sys.stderr)


def wordlist_writer(conf_obj: object, output_file: Path, file_mode: str):
    """
    Writes the resulting wordlist file from words stored in parsing set.

    :param conf_obj:  The program configuration instance.
    :param output_file:  The output wordlist file to write to.
    :param file_mode:  The file mode to open the output wordlist in.
    :return:  Nothing
    """
    try:
        # Write the result set to output wordlist #
        with output_file.open(file_mode, encoding='utf-8') as output_file:
            for string in conf_obj.parse_set:
                output_file.write(f'{string}\n')

    # If error occurs during file operation #
    except OSError as file_err:
        # Look up specific error with errno module #
        error_query(str(output_file), file_mode, file_err)
