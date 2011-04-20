#!/usr/bin/env python
import sys
import fileinput

if __name__=='__main__' :
    FIELD_INDEX = 0
    FIN = open(sys.argv[1],'r')
    FOUT = open("new_"+sys.argv[1], 'w')
    for line in FIN:
        if line.find('<field id=') > -1:
            pos = line.find("\"")
            pos = line.find("\"",pos+1)
            rest_attr = line[pos+1:]
            line = '{0}{1}'.\
                format("                <field id=\"{0}\"".format(FIELD_INDEX),\
                    rest_attr)
            FIELD_INDEX += 1
        FOUT.write(line)
        print line
    FIN.close()
    FOUT.close()
    #f.close()
