# cvgen

A program for generating a curriculum vitae.

Parameters are controlled via configuration files (cvdata.json, company.json, enclosure.json, cvgeometry.json, LaTeX\_cell\_styles.json, LaTeX\_preamble.json, and letter.txt) in the user's home directory (/home/user/.config/cvgen).
First-time launch creates config files with generic settings. Personal data is stored in cvdata.json, data of the company in company.json. The cv's layout is controlled by cvgeometry.json, LaTeX settings can be changed in LaTeX\_cell\_styles.json and LaTeX\_preamble.json. Letter.txt contains the text of the motivational letter.

Running cvgen generates a LaTeX file that makes use of the document class "standalone". The generated LaTeX code relies heavily on the TikZ package to create text boxes and graphical elements.

Compilation and opening of the resulting PDF file can be done automatically by command-line options. Descriptions of all options are displayed when calling the --help option.

