
import os
from collections import Counter
import matplotlib.pyplot as plt

import pandas 

file_name = 'C:\\Users\\surial\\Documents\\Projects\\smartmanuf\\smartsearch\\v2\\corpus_prahse\\pharase_text.txt'
file_object  = open(file_name, 'w')
valid_tag = ['PRD','UNT','SUB','NUM','BEN','CMN','CLA','PRO','ADP','RTB','STO','TRM']

for subdir, dirs, files in os.walk('C:\\Users\\surial\\Documents\\Projects\\smartmanuf\\smartsearch\\v2\\corpus'):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file
        #print (filepath)

        with open(filepath, 'r',encoding="utf8", errors='ignore') as content_file:

        #'''with open('/Users/surial/Documents/Projects/smartmanuf/smartsearch/v1/corpus/Sabiwhite PDS.txt', 'r') as content_file:'''
            content = content_file.readlines()
            for x in content:
                a = x.strip()
                if '\\' in a and '[' in a :
                    c = a.replace('\n', '')[a.find('[')-3:].split('\\')
                    for y in range(len(c)):
                        try:
                            if c[y][0] == ']':
                                if '[' in c[y-1]:
                                    final_string = (c[y-1]+ c[y][0])
                                    final_string = final_string.replace('[', ',')
                                    final_string = final_string.replace(']', '')
                                    if len(final_string.split()) < 4:
                                        tag_split =  final_string.split(',')[0]
                                        if tag_split in valid_tag:
                                            file_object.write(final_string+ '\n')
                        except:
                            pass
file_object.close()

list_tag =[]
with open(file_name, 'r') as fp:
    content = fp.readlines()
    for x in content:
        list_tag.append( x.split(',')[0])

tag_counter  = Counter(list_tag)
print(tag_counter)
plt.bar(range(len(tag_counter)), list(tag_counter.values()), align='center')
plt.xticks(range(len(tag_counter)), list(tag_counter.keys()))


plt.show()

