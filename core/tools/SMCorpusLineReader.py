import os, sys
import regex as rg
from .CorpusPedigree import CorpusPedigree
from .PedigreeVisualizer import PedigreeVisualizer

'''
    The corpus reader scans all text files in the designated corpus folder.
    The sentences and the phrases within those sentences in the corpus folder
    are marked with special wrapper tags to identify specific pharmaceutical
    expressions such as claims, benefits, ingredient, etc.

    The SMCorpusReader derives from nltk's CorpusReader instance and adds
    additional features on top of it. 
''' 

from nltk.corpus.reader.api import CorpusReader
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import pandas as pd
from .ClassifierMixin import ClassifierMixin

class SMCorpusLineReader(CorpusReader, ClassifierMixin):

    __slots__ = [
        '_repattern',       # Regex pattern that captures the sentence or phrase within tag demarcation.
        '_resubpatt',       # Regex pattern to replace tags from the sentence or phrase.
        '_sentclasses',     # A dictionary of tags and list of sents.
        '_phraseclasses'    # A dictionary of tags and list of phrases.

    ]
    
    def __init__(self, root):
        super(SMCorpusLineReader, self).__init__(root, ".*")
        self._repattern = r'(\\[A-Z]{3}\[)(.*)(\\\])' # recursive patterns like r'\\[A-Z]{3}\[(?>[^\\[A-Z]{3}\[\]]|(?R))*\]' is not working with python regex
        self._resubpatt = r'(\\[A-Z]{3}\[)|(\\\])'
        self._pdigreestruct = CorpusPedigree()
        self._sentclasses = dict()
        self._phraseclasses = dict()
        self._parse_corpus_sents()
    
    def __str__(self):
        return "SmartManuf Corpus Reader"


    def sents(self):
        ''' Returns a dictionary tags and sentences. '''
        return self._sentclasses

    def phrases(self):
        ''' Returns a dictionary tags and phrases. '''
        return self._phraseclasses

    def visualize(self):
        return PedigreeVisualizer('''pass pdgreestruct''')

    def _extract_classify_phrase(self):
        ''' 
            Extract the phrase and classify it.
            The data is returned in the following tuple form
            [
                (0, 'ROOT TAG', 'Sentence'),
                (1, 'NESTED TAG', 'Nested Phrase in the Sentence at root level'),
                ....
            ]
            TIP: Yield rows in the returned list instead of sending a fully loaded list.
        '''
        pass

    def _parse_corpus_sents(self):
        for ff in os.walk(self.root):
            # ff is a tuple of ('currdir', 'list of subdirs', 'list of files')
            # we are only concerned about files
            d,_,f = ff
            # open file and read line by line
            for filename in f:
                _, ext = os.path.splitext(filename)
                if ext != ".txt":
                    continue
                file = os.path.join(d,filename)
                with open(file, 'r') as file:
                    for line in file:
                        if line:
                            line = line.strip()
                            if line:
                                self._parse_corpus_rootsent(line.strip())


    def _parse_corpus_rootsent(self, sent):
        ''' Use regex pattern to parse a corpus sentence recursively and add them to our data structure '''
        if not sent:
            return
        for tleft, phrase, tright in self._rgtags.findall(sent):
            ph = self._clean_phrase(phrase)
            tag = self._strip_tag(tleft)
            # Add to the tree root
            self._add_to_tree(tag, ph, False) # TODO clean up sentences from tags.
            # parse the phrase again
            self._parse_corpus_phrases(phrase)

    def _parse_corpus_phrases(self, phrase):
        ''' Use regex pattern to parse a corpus sentence recursively and add them to our data structure '''
        if not phrase:
            return
        for tleft, ph, tright in self._rgtags.findall(phrase):
            ph = self._clean_phrase(ph)
            tag = self._strip_tag(tleft)
            self._add_to_tree(tag, ph, True) 
            # parse the phrase again
            self._parse_corpus_phrases(ph)

    def _clean_phrase(self, phrase):
        ''' Remove tags embedded in the sentence. '''
        return self._rgrepltags.sub('', phrase)

    def _strip_tag(self, tag):
        ''' Remove demarcations around the tag text. '''
        if not tag or not isinstance(tag, str):
            return tag
        return tag.lstrip('\\').rstrip('[')

    def _add_to_tree(self, tag, phrase, isnested):
        # when isnested is false, full sentence is processed, 
        # as soon isnested is true nested tags in the same sentence
        # are processed. Then isnested goes back to false again for 
        # for a full sentence.
        def insertindict(d, tag, phrase):
            if tag not in d:
                d[tag] = [phrase]
            else:
                d[tag].append(phrase)
        if isnested:
            insertindict(self._phraseclasses, tag, phrase)
        else:
            insertindict(self._sentclasses, tag, phrase)

