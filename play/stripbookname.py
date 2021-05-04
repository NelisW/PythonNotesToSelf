import glob
import re
import os

lstR = [' - libgen.li',' - libgen.lc','-Verlag Berlin Heidelberg)',' International Publishing',
        '-Verlag Berlin Heidelberg',' Singapore_Springer',', New Society Publishers',
        ', CreateSpace Independent Publishing Platform',', Random House',
        ', Packt Publishing Ltd',', Packt Publishing Pvt. Ltd.',', Packt Publishing',
        ', Routledge_Taylor & Francis Group',', Routledge',', Addison-Wesley',' Singapore_Springer',
        ', Springer US',
        ', Financial Times_Prentice Hall',', Skyhorse Publishing','-IEEE Press',
        ', Mc Graw Hill India','-Verlag Berlin Heidelberg',', Harper Design',
        ', Oxmoor House_Time Home Entertainment',', Publishing House W. Ennsthaler',
        ', HarperCollins_Harper Design',', PublishDrive',', Stanford University Press',
        ', DESIGN MEDIA PUBLISHING LIMITED',', Zuleika', ', Princeton Architectural Press',
        ', Links',', Think Publishing',', Universal Magazines',', Links International',
        ', Elsevier _ Architectural Press',', Quarry Books',', Springer',', Architectural Press',
        ', CRC Press',', Bloomsbury Publishing',', InTech',', Liaoning Science & Technology Pub. House',
        ', Jenny Stanford Publishing',', Wiley',', Tilt Development',', LST Publishing House, Professional Design press',
        ', Actrace_Profession Design Press Co., Ltd',', Artech House',' India Ltd._',' India',' International',
        ', Mcgraw-Hill',', China Machine Press'        ]

lstX = [r'\(Editor\)','\(auth\)','\(auth.\)','\(Author\)','\(author\)','\(Ed.\)',
        '\(eds.\)','^\[.*\]'
]

for fext in ['*.pdf','*.epub','*.djvu']:
    for name in glob.glob(fext):
        mname = name
        for bad in lstR:
            if bad in mname:
                mname = mname.replace(bad,'')
        for rex in lstX:
            if re.search(rex,mname):
                mname = re.sub(rex,'',mname)

        mname = re.sub('^\s*','',mname)


        os.rename(name,mname)
        print(mname)





