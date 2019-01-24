'''
    Running methods in this module can be used to visualize the sentence pedigree
    using graphviz

    https://graphviz.gitlab.io/_pages/Gallery/directed/lion_share.html

'''

from graphviz import Digraph

class PedigreeVisualizer(object):
    
    def view(self):
        s = Digraph('memorymodel', filename='memorymodel.gv', node_attr={'shape': 'record', 'rankdir':'LR', 'height' : '.1'})
        s.node('S1', ' {{ <f0> | { Enhances | Refines | Maintains} } } | { cell nucleus function | <f1> cell nucleus health } | for | { resilient skin | complexion | <f2> youthful skin } } ')
        #s.node('S2', ' { <f0> Refines  | skin | and | creates | a | flawless | { <f2> complexion } } ')
        #s.node('S3', ' { <f0> Maintains | { <f1> cell nucleus health } | to | ensure | { <f2> youthful skin }  }')
        s.node('CLA', 'CLA')
        #s.node('RTB', 'RTB')
        #s.node('BEN', 'BEN')
        s.edge('S1:f0','CLA')
        #s.edge('S2:f0','CLA')
        #s.edge('S3:f0','CLA')
        s.edge('S1:f1', 'RTB')
        #s.edge('S3:f1', 'RTB')
        s.edge('S1:f2', 'BEN')
        #s.edge('S2:f2', 'BEN')
        #s.edge('S3:f2', 'BEN')
        s.view()