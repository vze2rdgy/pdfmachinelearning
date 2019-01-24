import pandas as pd

class PedigreeMember(pd.Series):
    pass

class TagEdge(object):
    tag = None

class CorpusPedigree(object):
    """
    A fully constructed pedigree (inverted tree view) of the phrases collected from the corpus
    The top level of the inverted tree is a horizontal vector. Each member is an instance of PedigreeMember.
    The leaf node is the root tags (the root tags are placed around the entire sentence. The sub-tags are nested tags.

    Example tagged sentence 
    1. \CLA[Enhances \RTB[cell nucleus function] for \BEN[resilient skin\]\].
    2. \CLA[Refines skin and creates a flawless \BEN[complexion\]\].
    3. \CLA[Maintains \RTB[cell nucleus health\] to ensure \BEN[youthful skin\]\].

    Using a POS tagger, we can identify words which have similar parts of speech and bring them together. 
    Ex. Enhance, Refine and Maintain have same POS attribute.

    When search is done on a test sentence, we always utilize a bi-gram or tri-gram. Single words are not 
    used for categorization.

    ('Enhances cell nucleus function for resilient skin', 'CLA')
        [cell nucleus function] for resilient skin]
                    [resilient skin]

    The memory model will look like below

    [Enhances | cell | nucleus | function | resilient | skin |          ]
    [Refines                                          | skin |          ]
    [creates                              | flawless  | skin            ]
    [Maintains|                                                  health ]
    
    Edges are used to connect a phrase to a TAG.
    
    """






