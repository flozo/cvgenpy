#!/usr/bin/env python3

# Import modules

import argparse
import cvdata as cv
import geometry as geo
import functions as fn
import output as out
import os

# Version
version_num = '0.32'
version_dat = '2021-08-09'
version_str = '{} ({})'.format(version_num, version_dat)

def main():
    # Define argument parsers and subparsers
    parser = argparse.ArgumentParser(description='A program for generating CVs in LaTeX. Written by flozo.')

    parser.add_argument('-V', '--version', action='version', version='%(prog)s '+ version_str)
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='verbosity level (-v, -vv, -vvv): '
                        'default = single-line output, v = multi-line, vv = detailed, vvv = array output')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help=('disable terminal output (terminates all verbosity)'))
    parser.add_argument('-l', '--latex', action='store_true',
                        help='execute pdflatex after creating *.tex file')
    parser.add_argument('-L', '--language', choices=('de', 'en'), default='en',
                        help='set language (English=en, German=de)')
    parser.add_argument('-M', '--microtype', action='store_true',
                        help='use microtype package for fine tuning of type set')
    parser.add_argument('-d', '--draft', action='store_true',
                        help='Draft mode: highlight text fields')
    parser.add_argument('-m', '--metadata', action='store_true',
                        help='add PDF metadata')
    parser.add_argument('-s', '--show', action='store_true',
                        help='show pdf after executing pdflatex (implies -l)')
    # Make -e and -E mutually exclusive
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--enclosure-latex', dest='encl_latex', action='store_true',
                        help='include enclosure using LaTeX')
    group.add_argument('-E', '--enclosure-python', dest='encl_python', action='store_true',
                        help='include enclosure using Python')
    parser.add_argument('outfile', nargs='?', help='write to file')

    args = parser.parse_args()

    # Check verbosity level
    verbosity = args.verbose
    if args.quiet is True:
        verbosity = -1
    if verbosity >= 1:
        print(args)

    # Use config directory or create one
    config_dir = os.path.expanduser('~/.config/cvgen')
    fn.check_config_dir(config_dir)
    config_file_data = os.path.join(config_dir, 'cvdata.json')
    config_file_company = os.path.join(config_dir, 'company.json')
    config_file_geo = os.path.join(config_dir, 'cvgeometry.json')
    config_file_enclosure = os.path.join(config_dir, 'enclosure.json')
    config_file_letter = os.path.join(config_dir, 'letter.txt')
    config_file_preamble = os.path.join(config_dir, 'LaTeX_preamble.json')
    config_file_cell_styles = os.path.join(config_dir, 'LaTeX_cell_styles.json')
    config_file_layers = os.path.join(config_dir, 'LaTeX_layers.json')
    config_file_skills = os.path.join(config_dir, 'skills.json')
    fn.check_config_file(config_file_data)
    fn.check_config_file(config_file_company)
    fn.check_config_file(config_file_geo)
    fn.check_config_file(config_file_enclosure)
    fn.check_config_file(config_file_letter)
    fn.check_config_file(config_file_preamble)
    fn.check_config_file(config_file_cell_styles)
    fn.check_config_file(config_file_layers)
    fn.check_config_file(config_file_skills)
    text = fn.read_text(os.path.join(config_dir, 'letter.txt'))  
    text = fn.format_text(text)

    config_data = fn.read_config(config_file_data)
    config_geo = fn.read_config(config_file_geo)
    config_encl = fn.read_config(config_file_enclosure)

    # Check file extension
    outfile = str(args.outfile)
    if outfile[-4:0] != '.tex':
        outfile = outfile + '.tex'
    outfile = os.path.abspath(outfile)
    # Collect names of enclosed documents
    if args.language == 'en':
        encl = ['Curriculum vitae']
    elif args.language == 'de':
        encl = ['Lebenslauf']
    for enclosure in config_encl.keys():
        encl.append(enclosure)
    draft = args.draft
    if draft is True:
        print('[output] Option --draft is active.')
#            print('[output] Option --draft is active. Ignoring contradicting setting in cvgeometry.json: "draft": false')
    out.assemble_latex(outfile, version_str, config_file_geo, config_file_data, config_encl, text, args.microtype, args.metadata, encl, draft, args.encl_latex, config_file_preamble, config_file_cell_styles, config_file_company, args.language, config_file_layers, config_file_skills)
    # Messages and execution of pdfLaTeX/mupdf
    if verbosity >= 1:
        print('[output] LaTeX file {} created.'.format(outfile))
    if (args.latex or args.show) is True:
        output_dir = os.path.dirname(outfile)
        cmd = 'pdflatex -synctex=1 -interaction=nonstopmode -output-directory {} {}'.format(output_dir, outfile)
        if verbosity >= 1:
            print('[output] Executing pdfLaTeX: {} ...'.format(cmd))
        # redirect pdfLaTeX output to log file to enable true quiet mode
        if verbosity == -1:
            cmd = '{} > {}/pdfLaTeX_last_output.log'.format(cmd, config_dir)
        os.system(cmd)
        if verbosity >= 1:
            print('[output] ... done!')
    outfile_pdf = '{}.pdf'.format(outfile[0:-4])
    if args.show is True:
        if verbosity >= 1:
            print('[output] Opening PDF file via: mupdf {} ...'.format(outfile_pdf))
        os.system('mupdf {}'.format(outfile_pdf))
    if args.encl_python is True:
        if verbosity >= 0:
            print('[output] Option --enclosure-python is active. Using Python to include enclosure documents...')
        pdflist = [outfile_pdf]
        for pdf in config_encl.values():
            pdflist.append(pdf)
        complete_pdf = '{}_complete.pdf'.format(outfile[0:-4])
        if verbosity >= 1:
            print('[output] Concatenate PDFs: {} ...'.format(pdflist))
        fn.mergepdfs(pdflist, complete_pdf)
        if verbosity >= 1:
            print('[output] ... done!')


if __name__ == '__main__':
    main()

