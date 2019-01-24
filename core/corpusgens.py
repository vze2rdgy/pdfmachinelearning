''' Different classes that accepts an autotagger instance and converts
    a pdf-converted text file into a corpus file with required tags.
    After the file is tagged, it is pushed into review location.
'''

import pandas as pd
import io

class CorpusGenerator(object):
    __slots__ = [
        '_autotagger',
        '_txtstream',
        '_outstream',
        '_encoding' # default is ISO-8859-1 which is latin-1 or ascii
        ]
    def __init__(self, autotagger, txtfilestream, encoding):
        self._autotagger = autotagger
        self._txtstream = txtfilestream
        self._encoding = encoding
        self._outstream = None
        self._convertToCorpus();
        return 

    def _convertToCorpus(self):
        raise NotImplementedError("Derived class must implement this function.")

    def write(self, outfileName):
        with open(outfileName, 'wt', encoding=self._encoding) as outfile:
            outfile.write(self._outstream.getvalue())
        return

class DefaultCorpusGenerator(CorpusGenerator):

    # autotagger's getsents method -> [for pno, tagname, score, sent in data ]

    def __init__(self, autotagger, txtfilestream, encoding):
        CorpusGenerator.__init__(self, autotagger, txtfilestream, encoding)
        return

    def _convertToCorpus(self):
        # use _txtstream and _outstream
        # to reproduce output data exact look alike of input data (idem quod)
        # we have to go char by char
        
        # create a sent to tag dictionary
        sents = {sent : (score, tagname) for pno, tagname, score, sent in self._autotagger.getSents()}
        positions = {}
        instr = self._txtstream[1]
        for key, data in sents.items() :
            try:
                idx = instr.index(key)
                positions[idx] = (key, len(key))
            except ValueError as e:
                e

        self._outstream = io.StringIO()
        closeTagPos = -1
        for i, c in enumerate(instr):
            if i in positions:
                sent, l = positions[i]
                rank, tag = tagged[sent]
                if rank > .6 :
                    self._outstream.write("\\" + tag + "[")
                    closeTagPos = i + 1
            if i == closeTagPos:
                self._outstream.write("\\]")
            self._outstream.write(c)

def getCorpusGenerator(autotagger, txtfilestream, encoding = 'ISO-8859-1'):
    return DefaultCorpusGenerator(autotagger, txtfilestream, encoding)

