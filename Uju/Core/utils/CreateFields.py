#!/usr/bin/env python
import sys
import fileinput

if __name__=='__main__' :
    if len(sys.argv) != 3:
        print "Please input file and range of the fields"
        sys.exit(1)
    FIELD_INDEX = 0
    FIELD_RANGE = sys.argv[2]
    FIN = open(sys.argv[1],'r')
    FOUT = open("new_"+sys.argv[1], 'w')
    for line in FIN:
        infields = False
        if line.find('<fields total=') > -1:
            pos = line.find("\"")
            pos = line.find("\"",pos+1)
            rest_attr = line[pos+1:]
            line = '{0}{1}'.\
                format("               <fields total=\"{0}\"".format(FIELD_RANGE),\
                    rest_attr)
            infields = True
        FOUT.write(line)
        if infields == True:
            for i in range(int(FIELD_RANGE)):
                FOUT.write("                   <field id=\"{0}\"/>\n".format(i))
            infields = False
    FIN.close()
    FOUT.close()
    #f.close()
