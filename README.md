# Table Tennis Match Web Scraper

This is a Python script that scrapes Liga Pro table tennis match results and
exports the data as an Excel spreadsheet.

## Requirements

Download [ChromeDriver](https://sites.google.com/chromium.org/driver/downloads)
and [add to your
PATH](https://zwbetz.com/download-chromedriver-binary-and-add-to-your-path-for-automated-functional-testing/).

Mark scripts as executable:
``chmod +x mynamecase.py``
``chmod +x installmodules.py``

Using the package manager [pip](https://pip.pypa.io/en/stable/), either run the
`installmodules` script:
``./installmodules.py``

or manually install the following packages:

- requests: 
``pip install requests``

- pandas: 
``pip install pandas``

- BeautifulSoup: 
``pip install beautifulsoup4``

- selenium: 
``pip install selenium``

- openpyxl: 
``pip install openpyxl``

- xlrd: 
``pip install xlrd``

## Usage

In the directory containing the script:
```
./mynamecase.py

Enter date (YYYY-MM-DD): 2021-09-06
```
