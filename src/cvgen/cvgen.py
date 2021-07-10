#!/usr/bin/env python3

# Import modules

import argparse
import cvdata as cv
import geometry as geo
import functions as fn
import output as out
import os

# Version
version_num = '0.14'
version_dat = '2021-07-10'
version_str = '{} ({})'.format(version_num, version_dat)

def main():
    # Define argument parsers and subparsers
    parser = argparse.ArgumentParser(description='A program for generating CVs in LaTeX. Written by Johannes Engelmayer')

    parser.add_argument('-V', '--version', action='version', version='%(prog)s '+ version_str)
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='verbosity level (-v, -vv, -vvv): '
                        'default = single-line output, v = multi-line, vv = detailed, vvv = array output')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help=('disable terminal output (terminates all verbosity)'))
    parser.add_argument('-l', '--latex', action='store_true',
                        help='execute pdflatex after creating *.tex file')
    parser.add_argument('-s', '--show', action='store_true',
                        help='show pdf after executing pdflatex (implies -l)')
    parser.add_argument('-a', '--appendix', action='store_true',
                        help='include appendix pdfs')
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
    config_file_geo = os.path.join(config_dir, 'cvgeometry.json')
    fn.check_config_file(config_file_data)
    fn.check_config_file(config_file_geo)

    # Check file extension
    outfile = str(args.outfile)
    if outfile[-4:0] != '.tex':
        outfile = outfile + '.tex'
    outfile = os.path.abspath(outfile)
    out.assemble_latex(outfile, version_str, config_file_geo, config_file_data)
    # Messages and execution of pdfLaTeX/mupdf
    if verbosity >= 1:
        print('[output] LaTeX file {} created.'.format(outfile))
    if (args.latex or args.show) is True:
        output_dir = os.path.dirname(outfile)
        cmd = 'pdflatex -synctex=1 -interaction=nonstopmode -output-directory {} {}'.format(output_dir, outfile)
        if verbosity >= 1:
            print('[output] Executing pdfLaTeX: {} ...'.format(cmd))
        os.system(cmd)
        if verbosity >= 1:
            print('[output] ... done!')
    outfile_pdf = '{}.pdf'.format(outfile[0:-4])
    if args.show is True:
        if verbosity >= 1:
            print('[output] Opening PDF file via: mupdf {} ...'.format(outfile_pdf))
        os.system('mupdf {}'.format(outfile_pdf))
    config_geo = fn.read_config(config_file_geo)
    if args.appendix is True or config_geo['structure']['appendices'] is True:
        config_data = fn.read_config(config_file_data)
        if config_geo['structure']['appendices'] is False and verbosity >= 0:
            print('[output] Option --appendix is active. Ignoring contradicting setting in cvgeometry.json: "appendices": false')
        pdflist = [outfile_pdf]
        for pdf in config_data['Appendix'].values():
            pdflist.append(pdf['file'])
        complete_pdf = '{}_complete.pdf'.format(outfile[0:-4])
        if verbosity >= 1:
            print('[output] Concatenate PDFs: {} ...'.format(pdflist))
        fn.mergepdfs(pdflist, complete_pdf)
        if verbosity >= 1:
            print('[output] ... done!')


if __name__ == '__main__':
    main()

