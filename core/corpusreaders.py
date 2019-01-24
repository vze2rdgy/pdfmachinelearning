from .tools import SMCorpusDocumentReader
from . import BGConfig

class CorpusReaderBase(object):
    """ Corpus reader. This class has a way to monitor if corpus reader need to be
    loaded from a pickled state, or fresh reading from corpus location and pickle again.
    Fresh reading occurs when never pickled before or a new file is added to the corpus location.
    """
    __slots__ = [
        '_corpusLocation',
        '_tagset'
        ]


    def __init__(self, corpuslocation, tags):
        self._corpusLocation = corpuslocation
        self._tags = tags

    def Documents(self):
        raise NotADirectoryError()

    def Tags(self):
        return self._tagset



class DefaultCorpusReader(CorpusReaderBase):
    def __init__(self, corpuslocation, tags):
        super(DefaultCorpusReader, self).__init__(corpuslocation, tags)

    def Documents(self):
        return [] # yield

    def Sents(self):
        return [] # yield

    def Phrases(self):
        return [] # yield

def getCurrentReader(corpuslocation, tags):
    #return DefaultCorpusReader(corpuslocation, tags)
    return SMCorpusDocumentReader.SMCorpusDocumentReader(BGConfig.CorpusLocation, tags)