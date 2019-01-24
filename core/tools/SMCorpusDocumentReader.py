import os, sys
import regex as rg
from .ClassifierMixin import ClassifierMixin, SentenceSelections
import nltk
import io
import string
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SMCorpusDocumentReader(ClassifierMixin):
    """
        Reads and entire document for classification purpose.
        Only the tagged portions of the document is collected
        for classification purpose.
        The Documents() method returns a list of tuples 
        of ( tag, content).

        The tags are removed from the content.
    """
    __slots__ = [
        '_root',
        '_ext',
        '_rgBeginTag',
        '_rgEndTag'
        ]

    def __init__(self, root, tags, ext = ".txt"):
        ''' 
            Create instance. 
            The root is the root path to the location of corpus files.
            ext is the extension of the file. period should be provided. Use .* for all files.
        '''
        if not root:
            raise RuntimeError("root path is not provided.")
        if not os.path.exists(root):
            raise RuntimeError("root path not found.")

        ClassifierMixin.__init__(self, SentenceSelections.UseDocument, tags)

        self._root = root
        self._ext = ext

        self._rgBeginTag = rg.compile(self._begintagpattern, rg.IGNORECASE | rg.MULTILINE)
        self._rgEndTag = rg.compile(self._endtagpattern, rg.IGNORECASE | rg.MULTILINE)

        return

    def _extractDomain(self, file):
        ''' Extract the document's domain as provided by the corpus taggers.'''
        sDomain = ''
        startReading = False
        while True:
            s = file.read(1)
            if not s:
                break
            if s == '\\':
                sDomain += s
                startReading = True
                continue
            if s == '[':
                sDomain += s
                startReading = False
                break
            if startReading :
                sDomain += s
                continue
        logger.debug("File and its domain: %s/%s" % (file, sDomain))
        return sDomain, file.tell()


    def _cleanUpDocContent(self, contents):
        ''' 
            Clean up document content by removing carriage returns, 
            stop words, punctuations and other unwanted characters.
            Note, based on results, now we are only capturing
            tagged phrases in the document.
            Return the improved content.
        '''
        contents = self._clean_phrase(contents)
        inFile = io.StringIO()
        for w in ClassifierMixin.wordTokenize(contents):
            w = w.strip().lower()
            if w in string.punctuation:
                continue
            if w in self._engstopwords:
                continue
            inFile.write(w)
            inFile.write(' ')
        contents = inFile.getvalue()
        inFile.close()
        return contents

    def _collectTaggedItems(self, contents):
        ''' Returns a list of sentences and phrases which are tagged.'''
        for stag, ph, etag in self._rgtags.findall(contents):
            yield (stag, ph, etag)



    def _walkThruDocuments(self):
        ''' Walk through the corpus files in the root directory. Allow
            user provided function 'readHandle' to parse the file. 
        '''
        for ff in os.walk(self._root):
            d,_,f = ff # ff is a tuple (currdir, list of subdirs, list of files in curdir)
            for filename in f:
                _, fext = os.path.splitext(filename)
                if self._ext != '.*' and fext != self._ext:
                    continue
                filen = os.path.join(self._root, filename)
                stat = os.stat(filen)
                with open(filen, 'r', encoding='iso-8859-15') as file:
                    yield (file, stat, filename)

    def _makeDocCorpus(self):
        docs = []
        for file, stat, filename in self._walkThruDocuments():
            sDomain, position = self._extractDomain(file)
            if position == stat.st_size:
                # something is not right. Raise error
                raise RuntimeError('Failed to read the domain information from file ' + filen)
            contents = file.read()
            contents = contents.strip()
            contents = self._cleanUpDocContent(contents)
            # We have to ensure that first fiew char in the doc is \AAA|BBB[
            sDomain = sDomain.lstrip('\\').rstrip('[')
            for spl in sDomain.split(sep='|'):
                if "NON" in spl:
                    continue
                contents = self._rgBeginTag.sub('', contents)
                contents = self._rgEndTag.sub('', contents)
                docs.append((spl, contents, filename))
        return docs

    def _makeSentCorpus(self):
        ''' Collect and tag the phrases from the corpuses.'''
        phrases = set({})
        numOfFiles = 0
        for file, stat, _ in self._walkThruDocuments():
            numOfFiles += 1
            contents = file.read()
            contents = contents.strip()
            for ltag, ph, rtag in self._collectTaggedItems(contents):
                # remove special chars from phrases.
                # clean up ph from tags
                phcpy = ph
                ph = self._clean_phrase(ph)
                phrases.add((ltag.lstrip('\\').rstrip('['), self._rgEndTag.sub('', self._rgBeginTag.sub('', self.stemPhrase(ph)))))
                self._phraseDrillRecursive(phcpy, phrases)
        print("Processed {0} files and collected {1} tagged sentences.".format(numOfFiles, len(phrases)))
        return phrases


    def _makePhraseCorpus_old(self):
        ''' Collect and tag the phrases from the corpuses.'''
        phrases = set({})
        numOfFiles = 0
        for file, stat, _ in self._walkThruDocuments():
            numOfFiles += 1
            contents = file.read()
            contents = contents.strip()
            for ltag, ph, rtag in self._collectTaggedItems(contents):
                # remove special chars from phrases.
                phcpy = ph
                # clean up ph from tags
                ph = self._clean_phrase(ph)
                phrases.add((ltag.lstrip('\\').rstrip('['), self._rgEndTag.sub('', self._rgBeginTag.sub('', self.stemPhrase(ph)))))
                self._phraseDrillRecursive(phcpy, phrases)
        print("Processed {0} files and collected {1} tagged phrases.".format(numOfFiles, len(phrases)))
        return phrases

    def _makePhraseCorpus(self):
        ''' Collect and tag the phrases from the corpuses.'''
        valid_tag = ['PRD', 'UNT', 'SUB', 'NUM', 'BEN', 'CMN', 'CLA', 'PRO', 'ADP', 'RTB', 'STO', 'TRM']
        phrases = set({})
        numOfFiles = 0
        for file, stat, _ in self._walkThruDocuments():
            numOfFiles += 1
            contents = file.readlines()
            for line  in contents:
                line = line.strip()
                if '\\' in line and '[' in line :
                    line_formated = line.replace('\n', '')[line.find('[')-3:].split('\\')
                    for line_pos in range(len(line_formated)):
#                        try:
                            if line_formated and line_formated[line_pos] and line_formated[line_pos][0] == ']':
                                if '[' in line_formated[line_pos-1]:
                                    final_string = (line_formated[line_pos-1]+ line_formated[line_pos][0])
                                    final_string = final_string.replace('[', ',')
                                    final_string = final_string.replace(']', '')
                                    #if len(final_string.split()) < 4:
                                    if len(ClassifierMixin.wordTokenize(final_string)) < 4:
                                        ph = self._clean_phrase(final_string.split(",")[1])
                                        tag =  final_string.split(",")[0].strip()
                                        if tag in valid_tag:
                                            phrases.add((tag, self._rgEndTag.sub('', self._rgBeginTag.sub('', self.stemPhrase(ph)))))
#                        except Exception as e:
#                            logger.error(e)
        return phrases

    def _phraseDrillRecursive(self, phrase, phrases):
        ''' Dig deeper into phrase and collect nested phrases. '''
        for ltag, ph, rtag in self._collectTaggedItems(phrase):
            # remove special chars from phrases.
            phcpy = ph
            # clean up ph from tags
            ph = self._clean_phrase(ph)
            phrases.add((ltag.lstrip('\\').rstrip('['), self._rgEndTag.sub('', self._rgBeginTag.sub('', self.stemPhrase(ph)))))
            self._phraseDrillRecursive(phcpy, phrases)
        return

    def Documents(self):
        return self._makeDocCorpus()

    def Paras(self):
        pass

    def Sents(self):
        return self._makeSentCorpus()

    def Phrases(self):
        return self._makePhraseCorpus()

    def Tags(self):
        return self._tagset

def Test():
    rdr = SMCorpusDocumentReader('./corpus/')
    docs = rdr.Phrases()
    return


#if __name__ == "__main__":
    #Test()


