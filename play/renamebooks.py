import re
import os.path as path
import os

import pyradi.ryfiles as ryfiles
# rename YYYY_Book_somename.pdf to -somename-(YYYY).pdf

filenames = ryfiles.listFiles('.','*.pdf',recurse=0)

for fname in filenames:

    rtv = re.findall(r"(^\d{4})(_Book_)(.*)(\.pdf$)", fname)


    if len(rtv) > 0:
        name = re.sub(r"(\w)([A-Z])", r"\1 \2", rtv[0][2])
        newname = f' - {name}-({rtv[0][0]}){rtv[0][3]}'
        print(fname, newname)


        if not path.exists(newname):
            os.rename(fname,newname)
            # print(name)
            print(newname)
            # print('--------------------------')
        else:
            print(f'*** repeat name: {newname}')
            





