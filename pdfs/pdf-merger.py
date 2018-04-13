
"""
This is a helper script that assists to merge multiple pdf documents.
Tips: Ensure your pdf document sizes are of the same size: Eg: Letter/A4
example execution: python merger.py -p "folder with pdfs" -o "merged file name.pdf" -f *

"""

import os, argparse, sys
from PyPDF2 import PdfFileReader, PdfFileMerger

def process_pdfs(args):
    """
    Function that does the merging of the pdf files
    :param args: pdf_path, out_file, pdf_files[]
    :return: out_file created in pdf_path
    """
    pdf_files = args.pdf_files
    os.chdir(args.pdf_path)
    pwd = os.getcwd()

    # check if the user specifies all files
    if pdf_files[0] == '*':
        pdf_files = [f for f in os.listdir(pwd) if f.endswith('.pdf')]
        pdf_files.remove(args.out_file)

    for pdf_file in pdf_files:
        if not os.path.join(pwd, pdf_file):
            print("File does not exist. Exiting program")
            sys.exit(0)

    # merge the files
    merger = PdfFileMerger()
    print('The following files will be merged:')
    for file in pdf_files:
        print('-> {0}'.format(os.path.join(pwd, file)))
        merger.append(PdfFileReader(file), 'rb')
    merger.write(args.out_file)
    out_file_path = os.path.join(pwd, args.out_file)

    # confirm if out_file was successfully written
    if os.path.exists(out_file_path):
        print('File successfully written to:\n-> {0}'.format(out_file_path))
    else:
        print('Unable to write file to destination: \n->{0}.'.format(out_file_path))


def main():
    parser = argparse.ArgumentParser(description='Argument parser')
    parser.add_argument('-p', '--pdf_path', help='The path to the pdf documents')
    parser.add_argument('-o', '--out_file', help='The output file name')
    parser.add_argument('-f ', '--pdf_files', default="*", nargs='+', help='The files to merge or * for all pdf files')

    args = parser.parse_args()
    process_pdfs(args)


if __name__ == '__main__':
    main()