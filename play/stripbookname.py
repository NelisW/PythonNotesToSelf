import glob
import re
import os
from os import path

lstR = [' - libgen.li','- libgen.li',' - libgen.lc','- libgen.lc','- libgen.lc', '- libgen.li'
                ]

lstX = [r'\(Editor\)',r'\(editor\)','\(auth\)','\(auth.\)','\(Author\)','\(author\)','\(Ed.\)',
        '\(eds.\)','^\[.*?\]','^\(.*?\)',
]

for fext in ['*.pdf','*.epub','*.djvu','*.mobi','*.azw3']:
    for name in glob.glob(fext):
        mname = name
        for bad in lstR:
            if bad in mname:
                mname = mname.replace(bad,'')
        for rex in lstX:
            if re.search(rex,mname):
                mname = re.sub(rex,'',mname)

        # get rid of publisher name in date ()
        dategr = re.search('\((\d\d\d\d).*\)\s*\.', mname, re.IGNORECASE)
        if dategr:
            datestr = dategr.group(1)
            mname = re.sub('\(\d\d\d\d.*\)\s*\.',f'({datestr}).',mname)

        if not path.exists(mname):
            os.rename(name,mname)
            # print(name)
            print(mname)
            # print('--------------------------')
        else:
            print(f'*** repeat name: {mname}')
            





