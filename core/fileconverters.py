''' File converter factory and file converters for various file formats '''
import enum
import os
from tika import parser
import PyPDF4 as pyp
import contextlib
import logging

logger = logging.getLogger(__name__)


#class FileTypes(enum.Enum):
#    ''' Supported file converters '''
#    PDF = 1

@contextlib.contextmanager
def TikaPDFToTextConverter (filePath):
    parseddoc = parser.from_file(filePath)
    if parseddoc and "content" in parseddoc:
        try:
            encodedcontents = parseddoc["content"].strip().encode("iso-8859-15") #utf-8
        except Exception as e:
            encodedcontents = parseddoc["content"].strip().encode("utf-8")
        yield (0, encodedcontents)
    else:
        raise RuntimeError("Failed to parse and generate text content.")

@contextlib.contextmanager
def PyPDFToTextConverter(filePath):
    fd = open(filePath, 'rb')
    try:
        pdfreader = pyp.PdfFileReader(fd, strict=False)
        if pdfreader.isEncrypted:
            raise RuntimeError("PDF document is encrypted.")
        yield [(pagenum, pdfreader.getPage(pagenum).extractText()) for pagenum in range(pdfreader.getNumPages())]
        #r = [(pagenum, pdfreader.getPage(pagenum).extractText()) for pagenum in range(pdfreader.getNumPages())]
        #return r
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        fd.close()

@contextlib.contextmanager
def TextFileConverter(filePath):
    fd = open(filePath, 'r', encoding="ISO-8859-1") # ISO-8859-1 = latin1 (ascii), iso-8859-15 equivalent to utf8
    yield (0, fd.read())
    fd.close()

def getFileConverter(filePath):
    """Get an appropriate file converter"""
    #TODO: if performance of initializing a converter is an issue, cache in a dictionary.
    # Also at some point we have to identify the filetype by file's information rather than
    # relying on extension of the file.
    _, ext = os.path.splitext(filePath)
    if not ext or ext in ('.txt', '.text', '.csv'):
        return TextFileConverter(filePath)
    if ext.lower() == '.pdf':
        return PyPDFToTextConverter(filePath)
    else:
        raise ValueError("Unknown file type.")



