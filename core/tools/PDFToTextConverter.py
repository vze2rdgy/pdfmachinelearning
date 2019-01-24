import os
from tika import parser

class PDFToTextConverter(object):
    """
    PDF documents are converted to text files using this class. Utilizes Apache Tika converter.
    The input file's name is for conversion. For example, in input file name is 
    abc.pdf, then the output file's name is apc.txt.

    Also this class compares the files available in input path and output path. If output path
    already contains abc.txt, then, abc.pdf is not converted.
    """

    __slots__ = [
        '_inputPath',
        '_outputPath'
        ]

    def __init__(self, inputpath, outputpath):
        self._inputPath = inputpath
        self._outputPath = outputpath
        if not os.path.exists(self._outputPath):
            os.mkdir(self._outputPath)
        return

    def Convert(self, fileid = None):
        ''' Convert a PDF file from input directory. If fileid is specified, convert that file. 
        The fileid is a file's full name inside the input directory.
        Otherwise convert all files in the directory.'''
        filecontents = []
        if fileid:
            self._convertFile(self._inputPath, fileid, filecontents)
        else:
            for item in os.walk(self._inputPath):
                d, _, lf= item
                for filename in lf:
                    self._convertFile(d, filename, filecontents)
        return filecontents

    def _convertFile(self, d, filename, filecontents):
        # full path
        filepath = os.path.join(d, filename)
        # open the file with tika
        fn, ext = os.path.splitext(filepath)
        if ext != '.pdf' or self._IsFileAlreadyConverted(filename):
            return False
        parseddoc = parser.from_file(filepath)
        if parseddoc and "content" in parseddoc:
            encodedcontents = parseddoc["content"].strip().encode("iso-8859-15") #utf-8
            outputfile = os.path.join(self._outputPath, self._getTextFileName(filename))
            with open(outputfile, 'wb') as f:
                f.write(encodedcontents)
            filecontents.append((filename, encodedcontents))
        return True

    def _getTextFileName(self, filename):
        fn, ext = os.path.splitext(filename)
        return fn + ".txt"

    def _IsFileAlreadyConverted(self, fileName):
        fn = os.path.join(self._outputPath, self._getTextFileName(fileName) + ".txt")
        r = os.path.exists(fn)
        return r


if __name__ == "__main__":
    converter = PDFToTextConverter(
        r"C:\Users\sajia\Smartgaze LLC\Manpreet Kaur - PDFs\Pdfs", 
        r"C:\Users\sajia\Smartgaze LLC\Manpreet Kaur - PDFs\TestConvertedFiles"
        )
    for filename, converted in converter.Convert("TDS for VC2G.pdf"):
        print((filename, converted))




