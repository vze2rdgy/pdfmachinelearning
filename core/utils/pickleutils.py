import os, sys, pickle

def getPickledClassifier(ct, sel, root = None):
    ''' Load a pickled classifier instance. 
        @ct: Classifier class type.
        @sel: One of the values of ClassifierMixin.SentenceSelections.
    '''
    if not ct:
        raise ValueError("Please provide a classifier class type.")
    if not sel:
        raise ValueError("Provide a flag value from ClassifierMixin.SentenceSelections enum.")
    picklePath = os.path.join("." if not root else root, ct + '_' + str(sel) + '.clf')
    with open(picklePath, "rb") as f:
        return pickle.load(f)

def pickleClassifier(obj, root = None):
    if not obj:
        raise ValueError("obj must be a valid instance.")
    picklePath = os.path.join("." if not root else root, type(obj).__name__ + '_' + str(obj.getSelections()) + '.clf')
    with open(picklePath, "wb") as f:
        pickle.dump(obj, f)

def isPickled(ct, sel, root = None):
    picklePath = os.path.join("." if not root else root, ct + '_' + str(sel) + '.clf')
    return os.path.exists(picklePath)


