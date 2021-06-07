# this is experimental!!
# https://bibtexparser.readthedocs.io/en/master/

import bibtexparser
from bibtexparser.bwriter import BibTexWriter

def reformatbib(infile,outfile):

    with open(infile,'r') as bibfileIn:

        try:
            bib_database = bibtexparser.load(bibfileIn)
            writer = BibTexWriter()
            writer.align_values = True   
            writer.indent = '  '     # indent entries with spaces 
            # writer.comma_first = True  # place the comma at the beginning of the line
            with open(outfile, 'w') as bibfileOut:
                bibfileOut.write(writer.write(bib_database))
                print(f'Reformated {infile} written to {outfile}')
        except:
            print(f'{infile} not parsed')

reformatbib('allreferences.bib','allreferencesOut.bib')
reformatbib('allreferences02.bib','allreferences02Out.bib')
# reformatbib('allreferences03.bib','allreferences03Out.bib')
# reformatbib('allreferences04.bib','allreferences04Out.bib')
