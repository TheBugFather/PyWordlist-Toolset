<div align="center" style="font-family: monospace">
<h1>PyWordlist-Toolset</h1>
&#9745;&#65039; Bandit verified &nbsp;|&nbsp; &#9745;&#65039; Synk verified &nbsp;|&nbsp; &#9745;&#65039; Pylint verified 9.97/10
<br><br>

![alt text](https://github.com/ngimb64/PyWordlist-Toolset/blob/main/ScrapeParser.gif?raw=true)
![alt text](https://github.com/ngimb64/PyWordlist-Toolset/blob/main/BinParser.png?raw=true)
</div>

## Purpose
PyWordlist-Toolset features numerous modes for wordlist generation.

> **bin** - Parses words from binary file <br>
> **text** - Parses words from text file <br>
> **pdf** - Parses words from PDF file <br>
> **sanitize** - Sanitizes existing wordlist, removing punctuation, quotation marks, and excess whitespace <br>
> **scrape** - Takes website end points as input wordlists, scrapes webpage data to format wordlist <br>
> **gobuster** - Takes gobuster output as input, scrapes the endpoints to format wordlist

**Note**: scraping modes support IPv4 & IPv6 addressing or domain names.

Aside from the sanitizer, all scripts generate the wordlist in append mode.<br>
This allows the scripts to be executed in various combinations while still resulting in a single wordlist.

### License
The program is licensed under [GNU Public License v3.0](LICENSE.md)

### Contributions or Issues
[CONTRIBUTING](CONTRIBUTING.md)

## Prereqs
This program runs on Windows 10 and Debian-based Linux, written in Python 3.9 and updated to version 3.10.6

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Examples:<br> 
>       &emsp;&emsp;- Windows:  `python setup.py venv`<br>
>       &emsp;&emsp;- Linux:  `python3 setup.py venv`

- Once virtual env is built traverse to the (Scripts-Windows or bin-Linux) directory in the environment folder just created.
- For Windows, in the venv\Scripts directory, execute `activate` or `activate.bat` script to activate the virtual environment.
- For Linux, in the venv/bin directory, execute `source activate` to activate the virtual environment.
- If for some reason issues are experienced with the setup script, the alternative is to manually create an environment, activate it, then run pip install -r packages.txt in project root.
- To exit from the virtual environment when finished, execute `deactivate`.

## How to use

---
**Note**: python(3) means either python or python3 depending on Windows or Linux
> bin - `python(3) <input_bin_file> bin`

> text - `python(3) <input_text_file> text`

> pdf - `python(3) <input_pdf_file> pdf`

> sanitize - `python(3) <input_wordlist> sanitize`

> scrape - `python(3) --host <ip_address(4|6) | domain_name> --port <port_number> <input_wordlist> scrape`

> gobuster - `python(3) --host <ip_address(4|6) | domain_name> --port <port_number> <input_gobuster_output> gobuster`