#!/usr/bin/env bash
#SEDCMD="sed 's/\(fields\ total=\\"\([0-9]\)\\"\)/\1\ logical=\\"AND\\"/' $1"
path=$1
sed  -i 's/\(fields\ total=\"\([0-9]\)\"\)/\1\ logical=\"AND\"/' ${path}
sed -i  '7s/\(field\ id=\"\([0-9]\)\"\)/\1\ operator=\"Equal to\"/' ${path}
cat ${path}
