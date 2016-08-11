
# coding: utf-8

# In[20]:

import sys
import getopt
import os
import csv
"""
 Test of file to see if it confirms to the iPRG2016 study instructios
 Usage: checkiPRGResultFile -i input-file [-f fasta-file]
"""
class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

class WrongFormat(Exception):
    def __init__(self, msg,fields):
        self.msg = msg
        self.fields = fields
    
def getAllProteinNames(fastaFile):
    proteinNames = []
    with open(fastaFile,"r") as lines:
        for line in lines:
            if line[0]=='>':
                line = line.rstrip()[1:]
                proteinName = line.split(' ')[0]
                if proteinName[:4]=='HPRR':
                    proteinNames.append(proteinName)
    return proteinNames

def checkHeader(fields):
    if not len(fields)==13:
        raise WrongFormat(("Wong number of values in header (%i values)." % len(fields)),fields)
    if (not fields[0]=="FDR") and (not fields[0]=="PEP"):
        raise WrongFormat(("Header wrongly formated. Field 0 should either be PEP or FDR, it is currently given as \"%s\"."%fields[0]),fields)
    for sample in ['A','B','C','D']:
        for repl in range(1,4):
            name = sample +  str(repl)
            if not name in fields[1:]:
                raise WrongFormat("Could not find run %s in header" % name, fields)

def checkRow(fields,names):
    if not len(fields)==13:
        raise WrongFormat("Wong number of cells in row.", fields)
    if not fields[0] in names:
        raise WrongFormat("Protein name %s not recognized" % fields[0], fields)
    for field in fields[1:]:
        try:
            val = float(field)
        except TypeError:
            raise WrongFormat("The cell %s is not in floating point notation" % field, fields)
        if (val<0.0 or val>1.0):
            raise WrongFormat("The cell %s is not a value between 0.0 and 1.0" % field, fields)
            
def checkFile(resultFile="my_resultFile.txt",fastaFile="iPRG2016.fasta"):
    names = getAllProteinNames(fastaFile)
    with open(resultFile,"r") as inFile:
        csvReader = csv.reader(inFile, delimiter = '\t',quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        checkHeader(csvReader.next())
        for fields in csvReader:
            checkRow(fields,names)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hi:f:", ["help","test-file","fasta-file"])
        except getopt.error, msg:
             raise Usage(msg)
        checkFile()
        return
    except WrongFormat, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, " ".join(err.fields)
        return 3
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())

                



# In[21]:

main(["./my_resultFile.txt"])


# In[ ]:



