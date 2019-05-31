"""
This module contains several functions for extracting
data from PDF's using either the tabula python package or
the command line tool tesseract.
"""

import pandas as pd
import numpy as np
from wand.image import Image
import os
import subprocess
from PyPDF2 import PdfFileWriter, PdfFileReader
from tabula import convert_into


def pdf2csv():
    """
    Converts pdf tables to .csv files. Use "lattice" if
    the table has borders, use "stream" if not.
    :return:
    """
    while True:
        lattice = str(input("Lattice? (yes/no): ")).lower()
        if lattice in ['yes', 'y']:
            lattice = 'True'
            break
        elif lattice in ['no', 'n']:
            lattice = 'False'
            break
        else:
            print("Please try again.")

    while True:
        stream = str(input("Stream? (yes/no): ")).lower()
        if stream in ['yes', 'y']:
            stream = 'True'
            break
        elif stream in ['no', 'n']:
            stream = 'False'
            break
        else:
            print("Please try again.")

    for file in os.listdir('.'):
        filepath, ext = os.path.splitext(file)
        path, filename = os.path.split(filepath)
        if ext == '.pdf':
            convert_into(file, filename[:14] + '.csv',
                         output_format='csv',
                         stream=stream, lattice=lattice)

    return lattice, stream


def csv2exc():
    """Converts the .csv to .excel file"""
    for file in os.listdir('.'):
        filename, ext = os.path.splitext(file)
        if ext == '.csv':
            df = pd.read_csv(file, encoding='utf8', engine='python')
            writer = pd.ExcelWriter(filename + '.xlsx')
            df.to_excel(writer, 'sheet1', index=False)
            writer.save()


def convert_pdf():
    """
    batch convert pdf to png to prepare for OCR extraction. move this
    script to the directory containing PDFs, all PDFs will be 
    converted.
    
    """
    
    img_type = input("Would you like greyscale? (y/n)")
    for file in os.listdir('.'):
        basename = os.path.splitext(file)[0]
        ext = os.path.splitext(file)[1]
        if ext == ".pdf":
            with Image(filename=file, resolution=600) as img:
                img.format = 'png'
                if img_type.lower() == "y" or img_type.lower() == "yes":
                    img.type = 'grayscale'
                img.units = 'pixelsperinch'
                img.save(filename='{}.png'.format(basename[:14]))


def ocr():
    """
    Convert PDF to TXT file using Tesseract.
    """
    
    for file in os.listdir('.'):
        basename, ext = os.path.splitext(file)
        ext = os.path.splitext(file)[1]
        if ext == '.png':
            subprocess.call(['tesseract', file, basename])  


def wrangle(filename, num_columns_headers, num_columns_values):
    """
    TXT is converted to EXCEL file using pandas.
    num_column_headers - the column count from the right for the header rows
    num_column_values - the column count from the right for values rows.
    These are distinguished due to RPD column. RPD tends to add column
    for the values, but not the headers. 
    """
    basename, ext = os.path.splitext(filename)
    df = pd.read_table(filename, header=None)
    print(df)
#  Each line of the text file is imported into a DF as the first column
    df.rename(columns={df.columns[0]:0}, inplace=True)
#  The first item of each line is copied to the second column

    split_list = ['Total', 'Tota|', 'Methyl', 'Methy|' 'Ethy|', 'EPH', 'Dimethyl', 'Diethyl',
                  'Dimethy|', 'Benzyl', 'Benzy|', 'Aroclor', 'Diethy|', 'Vinyl', 'Viny|',
                  'Allyl', 'Sodium', 'Propylene', 'Nitrotoluene', 'Nitrophenol', 'Nitroaniline',
                  'Methylphenol', 'Methylaniline', 'Maleic', 'Ma|eic','LEPH', 'HEPH', 'LEPHs',
                  'HEPHs', 'Carbon']

    def smart_split(x):
        if len(x.split()) > 1 and ((x.split()[0] in split_list) or x.split()[0][-1] == ','):
            return x.split()[0] + ' ' + x.split()[1]
        elif len(x.split()) > 0:
            return x.split()[0]
        else:
            return np.nan

    df[1] = df[0].map(lambda x: smart_split(x))
#  Prints the first 20 lines, so the split between headers and values can be determined
    print(df.head(20))
    num_rows = int(input("Cutoff row for headers?"))

#  Rows designated as the headers
    df_upper = df.iloc[:num_rows]

#  Rows designated as the values
    df_lower = df.iloc[num_rows:]  
    
#  Determines what's printed in the third column onwards for the header
    for x in range(2, 2 + num_columns_headers):            
        y = x - 2 - num_columns_headers
        df_upper[x] = df_upper[0].map(lambda x: x.split()[y] if len(x.split()) >= num_columns_headers else np.nan) 

#  Determines what's printed in the third column onwards for the values 
    for x in range(2, 2 + num_columns_values):
        y = x - 2 - num_columns_values
        df_lower[x] = df_lower[0].map(lambda x: x.split()[y] if len(x.split()) >= num_columns_values else '** missing **')        



    df_joined = df_upper.append(df_lower)
    df_joined.sort_index(axis=1, inplace=True)
    
    writer = pd.ExcelWriter('{}.xlsx'.format(basename))
    df_joined.to_excel(writer, 'sheet1')
    writer.save()


def extract_pages():
    """
    Extract select pages from PDFs with tables. This function is applied to all 
    PDFs in the current folder.
    """
    area = input("What is the Site area code (5 alphanumeric characters)?: ")
    
    filelist = [f for f in sorted(os.listdir('.')) if f[-3:].lower() == 'pdf']
    for file in filelist:
        print(file)
        report_number = input("What is the report number? (eg. 001, 's' to skip): ")
        
        if report_number != 's':
            page_nums = input("Please list pages with tables: ")
            page_nums_list = [int(s) for s in page_nums.split(",")]
            basename, ext = os.path.splitext(file)
            try:
                inputpdf = PdfFileReader(open(file, 'rb'))
                for page in page_nums_list:
                    output = PdfFileWriter()
                    print(page)
                    output.addPage(inputpdf.getPage(page - 1))
                    if 10 <= page < 100:
                        page_format = '0' + str(page)
                    elif 1 <= page < 10:
                        page_format = '00' + str(page)
                    else:
                        page_format = page
                    with open("{}_{}_p{}-{}.pdf".format(area, report_number, page_format, basename), "wb") as outputStream:
                        output.write(outputStream)
            except:
                print('PDF file encrypted, cannot extract')


def concat_text():
    """
    Join individual text files with page numbers indicated
    """
    filelist = [f for f in sorted(os.listdir('.')) if f[-3:].lower() == 'txt' or f[-3:].lower() == 'csv']
    with open('report.txt', 'w') as outfile:
        for fname in filelist:
            with open(fname) as infile:
                outfile.write("--------------------\n **** Page {} ****\n--------------------\n\n".format(fname[11:14]))
                for line in infile:
                    outfile.write(line)

