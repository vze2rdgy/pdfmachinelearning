import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt
import csv
from nltk.tokenize import sent_tokenize
import re 
import nltk

#converts pdf, returns its text content as a string
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    codec = 'utf-8'
    output = io.StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb',  errors='ignore')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text 


file_dir = 'C:\\Users\\surial\\Documents\\Projects\\pdf_2018_11_28'
os.chdir(file_dir)
#print (os.listdir("."))
sent_tokenize_list = []
for file in os.listdir("."):
    if file.endswith(".pdf"):
        pdf_file1 = file_dir + '\\' + file
        pdf_file2 = file_dir + '\\' + file[:-3]+ 'txt'
        pdf_file3 = file_dir + '\\' + file[:-3]+ 'csv'
        print(pdf_file1)
        print(pdf_file2)
        a = convert(pdf_file1)
        file = open(pdf_file2,'w') 
        file.write(a) 
        file.close() 


corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader("/Users/surial/Downloads/prodpdfs2", ".*\.txt")
        #corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader('',pdf_file2)
print ("ACCESSING SENTENCES")

sentences=corpus.sents()
print(pdf_file3)
with open(pdf_file3, 'w') as resultFile:
    print(pdf_file3)
    wr = csv.writer(resultFile, dialect='excel')
    for x in sentences:
        y1 = ' '.join(x)
        y1 = ''.join(e for e in y1 if e in '''"#%&'()*+,-./0123456789:;<=>@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]_abcdefghijklmnopqrstuvwxyz| ''')
        wr.writerow([y1,]) 
        print(y1)
             
print('******DONE************')
