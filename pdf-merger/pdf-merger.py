
"""
This is a helper script that assists to merge multiple pdf documents.
Ensure your pdf document sizes are of the same size: Eg: Letter/A4

example execution:
-> python merger.py -p "folder with pdfs" -o "merged file name.pdf" -f *
-> python merger.py -p "folder with pdfs" -o "merged file name.pdf" -f ab.pdf 1.pdf 01.pdf
"""

import os
import sys

import argparse
import logging
from PyPDF2 import PdfFileReader, PdfFileMerger

logger = logging.getLogger(__name__)
logging.basicConfig(filename='pdf-merger.log',
                    level=logging.INFO,
                    filemode='w',
                    format='%(asctime)s | %(levelname)s | %(message)s')

def process_pdfs(args):
    """
    Function that does the merging of the pdf files
    :param args: pdf_path, out_file, pdf_files[]
    :return: out_file created in pdf_path
    """

    if os.path.exists(args.pdf_path):
        logger.info('Valid pdf_path supplied')
        os.chdir(args.pdf_path)
        pwd = os.getcwd()
        out_file_path = os.path.join(args.pdf_path, args.out_file)
        if os.path.exists(out_file_path):
            os.remove(out_file_path)
            logger.info('Removed existing out_file')
    else:
        logger.critical('pdf_path supplied: "{}" does not exist. Exiting program!'.format(args.pdf_path))
        sys.exit(0)

    # check if the user specifies all files
    if args.pdf_files[0].lower() == 'all':
        args.pdf_files = [f for f in os.listdir(args.pdf_path) if f.endswith('.pdf')]
        logger.warning('Searching folder for pdf files as none were supplied')
        if len(args.pdf_files) <= 1:
            logger.critical('Not enough pdf file found. Exiting program!')
            sys.exit(0)

    # merge the files
    merger = PdfFileMerger()
    logger.info('The following files will be merged:')
    for file in args.pdf_files:
        logger.info('-> {0}'.format(os.path.join(pwd, file)))
        merger.append(PdfFileReader(file), 'rb')
    merger.write(out_file_path)
    logger.info('File written to: {}'.format(out_file_path))

def main():
    parser = argparse.ArgumentParser(description='Argument parser')
    parser.add_argument('-p', '--pdf_path', help='The path to the pdf documents')
    parser.add_argument('-o', '--out_file', help='The output file name')
    parser.add_argument('-f ', '--pdf_files', default="all", nargs='+', help='The files to merge or * for all pdf files')

    args = parser.parse_args()

    if len(sys.argv) >= 2:
        logger.info('Beginning program')
        process_pdfs(args)
    else:
        logger.critical('No arguments parsed. Exiting program!')
        sys.exit(0)


if __name__ == '__main__':
    main()
