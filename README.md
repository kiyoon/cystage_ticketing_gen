# Description

CY:Stage ticketing notification generator, written in python 3. It generates notification cards (pictures) for CY:Stage Facebook page uploads. 

Author: Kiyoon Kim (yoonkr33@gmail.com)

# Dependencies

- Python 3
- Pillow (`pip install Pillow`)

This program is tested under Windows 10.

# Usage

You need 3 items in order to execute.

- ticketing_gen.py
- input.csv (ANSI encoding)
- res (directory)

Other folders or files are not necessarily needed. `reference` contains reference pictures made with Photoshop, `sample` contains sample output of this program. 

You only have to change `input.csv` as desired.

## Format of input.csv

We'll use Microsoft Excel standard for specifying rows and columns. For example, A2 means 2nd row, 1st column.

### A column

- A1: must contain the first date, in a YYYYMMDD format. B1, C1, D1, ... should be empty. To put it another way, the first row should NOT contain any other information than date, at any other columns. This field CANNOT be empty.
- Other rows: it can be either time, empty, or "N" value. N value ends the day and starts next day. If N value is present at a certain row, that row should NOT contain any other information at any other columns.

### B column

Writes in a body with normal black font.

Example entry: Musical  
Desired output: Musical

Example entry: Schedule: 1/13(Sat)~1/16(Tue)  
Desired output: Schedule: 1/13(Sat)~1/16(Tue)

### C column

Writes in a body with bold and blue font, with surrounding angle brackets. Aimed for writing names of plays.

Example entry: Cats  
Desired output: <span style="color:blue">**&lt;Cats&gt;**</span> (with blue text)

### D column

Writes in a body with normal black font. Works the same as B column, but puts text after C column's entry.

Example entry: final  
Desired output: final

### E column

Writes in a body with pink-backgrounded white font. Aimed for writing discount informations.

Example entry: Undergraduate discount  
Desired output: <span style="background-color:rgba(234, 104, 162, 1); color:white">&nbsp;Undergraduate discount </span> (with white text, pink background)

## Executing program

When formatting `input.csv` is done, execute in a command line prompt as follows:

`python ticketing_gen.py`

Output files will be generated in the same folder.
