

import pyradi.ryfiles as ryfiles
import regex

texfiles = ryfiles.listFiles('.','*.tex')
# print(texfiles)

lensel = 20

dPairs = {}
p = regex.compile(r'\\url\{(.+?)\}')
for texfile in texfiles:
    with open(texfile,'r') as fin:
        ifchanged = False
        filelines = []
        lines = fin.readlines()
        for line in lines:
            urls = p.findall(line)
            if len(urls) > 0:
                for url in urls:
                    # clean up the URL removing some  chars
                    tmpn = ryfiles.cleanFilename(url, removestring =" -_%:/,.\\[]<>*?#!'\"=&")
                    # get rid of http(s)
                    tmpn = tmpn.replace('https','').replace('http','')
                    # make long enough string
                    while len(tmpn) < lensel:
                        tmpn = tmpn + tmpn
                    #build cite key from start and end of string
                    citename = tmpn[0:lensel] + tmpn[-lensel:]
                    # append to the dict
                    if url not in dPairs:
                        dPairs[url] = citename
                    # build the new line. get rid of [] if present
                    line = line.replace(f'[\\url{{{url}}}]',f'\\cite{{{citename}}}')
                    if url in line:
                        line = line.replace(f'\\url{{{url}}}',f'\\cite{{{citename}}}')
                    ifchanged = True
            #store to write later
            filelines.append(line)
    if ifchanged:
        print(f'writing to {texfile}')
        with open(texfile,'w') as fout:
            fout.writelines(filelines)

with open('bibtexfile.bib','w') as fout:

    for key in dPairs:
        # print(key,dPairs[key])

        rstr = f"""
@misc{{{dPairs[key]},
  author         = {{}},
  title          = {{}},
  url            = {{{key}}},
  year           = {{2021}},
}}

"""
        fout.write(rstr)
        # print(rstr)


# print(dPairs)

