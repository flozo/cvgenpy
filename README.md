# cvgen

A program for generating a curriculum vitae.

Parameters are controlled via configuration files cvdata.json and cvgeometry.json in the user's home
directory (/home/user/.config/cvgen). First-time launch creates config files with generic settings.
While cvdata.json contains personal data, i.e., the content of the cv, cvgeometry.json controls the
cv's layout.

Running cvgen generates a LaTeX file that makes use of the document class standalone.
The LaTeX code relies heavily on the TikZ package to create text boxes and graphical elements.

Compilation and opening of the resulting PDF file  can be done automatically by command-line options.

