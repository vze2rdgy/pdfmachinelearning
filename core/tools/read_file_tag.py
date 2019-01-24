import os

file_object  = open('/Users/surial/Documents/Projects/smartmanuf/smartsearch/v1/corpus_prahse/pharase_text.txt', 'w')

for subdir, dirs, files in os.walk('/Users/surial/Documents/Projects/smartmanuf/smartsearch/v1/corpus'):
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
                                    print(final_string)

                                    file_object.write(final_string+ '\n')
                        except:
                            pass
file_object.close()