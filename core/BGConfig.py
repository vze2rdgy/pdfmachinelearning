import os

ROOTDIR	= "." #"/home/iclapadm/Documents/smf"

DropLocation    =  os.path.join(ROOTDIR, "drop")        #Auto tagger drops newly tagged file in this location
ConvertLocation = os.path.join(ROOTDIR, "ctxt")         # the converted files is created here.
StoreLocation   =  os.path.join(ROOTDIR, "store")       # this is where all the documents from suppliers resides inside their supplier id.
ReviewLocation  = os.path.join(ROOTDIR, "review")       #Location where experts review a tagged document
CorpusLocation  = os.path.join(".", "corpus")       #The reviewed file is then dropped into corpus location if review succeeded. Otherwise drop back in this location after corrections.
FailedLocation  = os.path.join(ROOTDIR, "failed")       # files failed to convert or tag are moved here.
PickledClassifiers = os.path.join(".", "pickles", "classifiers")
DBConnectionStr = "postgres://{}:{}@{}/iclap"       # Database connection string.
RebuildTrainingset = False      # tell the process if the training set needs to be rebuilt each time the process starts.
Phrase_Tags     = ['PRD', 'UNT', 'SUB', 'NUM', 'BEN', 'CMN', 'CLA', 'PRO', 'ADP', 'RTB', 'STO', 'TRM']
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])

def CreateFolders():
    folders = [DropLocation, ConvertLocation, StoreLocation, ReviewLocation, CorpusLocation, FailedLocation]
    for folder in folders:
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except FileExistsError as e:
                pass

def CreateAFolder(path):
    if path:
        try:
            os.makedirs(path)
        except FileExistsError as e:
            pass
