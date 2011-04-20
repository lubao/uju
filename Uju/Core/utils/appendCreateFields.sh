#!/usr/bin/env bash
path=$1
sed -i '/<fields\ total=\"-1\"\/>/a\
\t\t    <field id=\"0\"\/>\
\t\t    <field id=\"1\"\/>\
\t\t    <field id=\"2\"\/>\
\t\t    <field id=\"3\"\/>\
\t\t    <field id=\"4\"\/>\
\t\t    <field id=\"5\"\/>\
\t\t    <field id=\"6\"\/>\
\t\t    <field id=\"7\"\/>\
\t\t<\/fields>' ${path}
cat ${path}
