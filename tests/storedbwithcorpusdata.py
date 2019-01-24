from core import BGConfig
import os
import regex as rg
from nltk.corpus import stopwords as spw
from core.tools.ClassifierMixin import ClassifierMixin
import string
from core.data import api
from core.data import models

begintagpattern = r'\\[A-Za-z]{3}\['    # TODO: if not used remove these two variables
endtagpattern = '\\\]' # TODO: if not used remove these two variables
rgtags = rg.compile(r'(\\[A-Za-z]{3}\[)(.*)(\\\])', rg.IGNORECASE | rg.MULTILINE)
rgBeginTag = rg.compile(begintagpattern, rg.IGNORECASE | rg.MULTILINE)
rgEndTag = rg.compile(endtagpattern, rg.IGNORECASE | rg.MULTILINE)
rgrepltags = rg.compile(r'(\\[A-Za-z]{3}\[)|(\\\])', rg.IGNORECASE | rg.MULTILINE)
engstopwords = None
stemmer = None

def clean_phrase(phrase):
    global engstopwords
    ''' Remove tags embedded in the sentence. '''
    ph = rgrepltags.sub('', phrase)
    if not engstopwords:
        engstopwords = spw.words('english')
    cleaned = ''
    for w in ClassifierMixin.wordTokenize(phrase): #ph.split():
        w = w.strip().lower()
        if w in string.punctuation:
            continue
        if w not in engstopwords:
            cleaned += w
            cleaned += ' '
    cleaned = cleaned.strip()
    return cleaned

def collectTaggedItems(contents):
    ''' Returns a list of sentences and phrases which are tagged.'''
    for stag, ph, etag in rgtags.findall(contents):
        yield (stag, ph, etag)

def stemPhrase(sentorphrase, stemmertype = 'porter'):
    ''' 
    Stemming is the process of removing morphological affixes from each
    word in a phrase or sentence. Eg. Enhances => Enhanc, nucleus => nucleu
    This is useful when you want to train a dataset without being concerned
    about a word's different forms (presentense, pastense, noun, etc.)
    see: http://www.nltk.org/howto/stem.html
    '''
    import nltk.stem as stems
    global stemmer
    if not stemmer:
        if stemmertype == 'porter':
            stemmer = stems.porter.PorterStemmer()
        else:
            stemmer = stems.snowball.SnowballStemmer("english")
    newphrase = ''
    #toks = wordTokenize(sentorphrase)
    #toks1 = sentorphrase.split()
    for w in ClassifierMixin.wordTokenize(sentorphrase):
        newphrase += stemmer.stem(w)
        newphrase += ' '
    return newphrase.rstrip()


def phraseDrillRecursive(phrase, phrases):
    ''' Dig deeper into phrase and collect nested phrases. '''
    for ltag, phrase, rtag in collectTaggedItems(phrase):
        # remove special chars from phrases.
        phcpy = phrase
        # clean up ph from tags
        ph = clean_phrase(phrase)
        ph = rgEndTag.sub('', rgBeginTag.sub('', stemPhrase(ph)))
        phrase = rgEndTag.sub('', rgBeginTag.sub('', phrase))
        #print("\t\t" + ph)
        phrases.add((ltag.lstrip('\\').rstrip('['), ph, phrase))
        phraseDrillRecursive(phcpy, phrases)
    return

ext = ".txt"
numOfFiles = 0
docphrases = {}

for ff in os.walk(BGConfig.CorpusLocation):
    root = BGConfig.CorpusLocation
    d,_,f = ff # ff is a tuple (currdir, list of subdirs, list of files in curdir)
    for filename in f:
        _, fext = os.path.splitext(filename)
        if ext != '.*' and fext != ext:
            continue
        filen = os.path.join(root, filename)
        stat = os.stat(filen)
        print(filename)
        with open(filen, 'r', encoding='iso-8859-15') as file:
            numOfFiles += 1
            contents = file.read()
            contents = contents.strip()
            phrases = set({})
            for ltag, phrase, rtag in collectTaggedItems(contents):
                # remove special chars from phrases.
                # clean up ph from tags
                phcpy = phrase
                ph = clean_phrase(phrase)
                ph = rgEndTag.sub('', rgBeginTag.sub('', stemPhrase(ph)))
                phrase = rgEndTag.sub('', rgBeginTag.sub('', phrase))
                #print("\t" + ph)
                phrases.add((ltag.lstrip('\\').rstrip('['), ph, phrase))
                phraseDrillRecursive(phcpy, phrases)
            docphrases[filename] = phrases

# upload to database. supplier id defaulting to 1
api.seedDb()

db = api.DBSession.Create()
dbsession = db.getSession()

def getTag(tag):
    return dbsession.query(models.Tag).filter(models.Tag.Name==tag).first()

def getTagClass(classname):
    return dbsession.query(models.TagClass).filter(models.TagClass.Name==classname).first()

for f, phrases in docphrases.items():
    doc = models.Document(SupplId=1, Domain='SKN', FilePath=f)
    dbsession.add(doc)
    for tag, _, ph in phrases:
        metadata = models.DocMetaData(tag=getTag(tag), tagClass=getTagClass('Sentence'), Score=1.0, TagData=ph, PageNo=0, Offset=0)
        doc.TagMetaData.append(metadata)
    db.Commit()
