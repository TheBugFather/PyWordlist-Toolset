<div align="center" style="font-family: monospace">
<h1>PyWordlist-Toolset</h1>
&#9745;&#65039; Bandit verified &nbsp;|&nbsp; &#9745;&#65039; Synk verified &nbsp;|&nbsp; &#9745;&#65039; Pylint verified 9.97/10
<br><br>

![alt text](https://github.com/ngimb64/PyWordlist-Toolset/blob/main/ScrapeParser.gif?raw=true)
![alt text](https://github.com/ngimb64/PyWordlist-Toolset/blob/main/BinParser.png?raw=true)
</div>

## Purpose
PyWordlist-Toolset features numerous tools to create and format custom wordlists:

> binParser.py  -  Generates wordlist from arg binary file contents<br>
> fileParser.py  -  Generates wordlist from arg text file contents<br>
> sanitizer.py  -  Strips leading/trailing whitespace, and punctuation/quotation from string ends on arg wordlist<br>
> scrapeParser.py  -  Generate wordlist from scraped web data from arg url list

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
- Open a shell (cmd or terminal)
- Change directory to PyWordlist-Toolset
- For bin and file parser, move bin or file to be parsed in program directory
- For sanitizer, move the wordlist to be sanitized in program directory
- For scrape parser, set the IP/Domain and Protocol in program header<br>
<br>

Execution syntax:<br>

`binParser.py <binary filename>`<br>
`fileParser.py <text filename>`<br>
`sanitizer.py <wordlist name>`<br>
`scrapeParser.py <url list>`