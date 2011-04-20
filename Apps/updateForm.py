'''
Created on Oct 25, 2009

@author: paul
'''
#! /usr/bin/python
import MySQLdb,sys
from xml.sax.handler import ContentHandler
from xml.sax import parse
import os
import logging

_logger = logging.getLogger("mx.org.came.Schema.updateForm")

class schemaReader():
    global myHandler

    def parseFile(self,path):
        self.myHandler=FormHandler()
        with open("{0}".format(path),'r') as f:
            parse(f,self.myHandler)
            f.close()

    def getFormDict(self):
        return self.myHandler.formDict
    
class FormHandler(ContentHandler):
    #These are CLASS VARIABLE By default is PUBLIC
    global formDict
    
    def __init__(self):
        self.formDict={}
    
    def startElement(self,name,attrs): 
        if name=='form': 
            nameList=attrs.getNames()
            for i in range(len(nameList)):
                self.formDict[nameList[i]]=attrs.getValue(nameList[i])

def createFormInfoDB():
    sql='''
        CREATE DATABASE `FormInfo`
        '''
    #print sql
    try:
        conn=MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="password")
        cursor=conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()
        return True
    except MySQLdb.Error ,e:
        ret="Error %d: %s" % (e.args[0],e.args[1])
        _logger.exception(ret)
        return False
    
def createFormInfoTable():
    sql='''
        CREATE TABLE `FormInfo`.`Info` (
                `aid` INT NOT NULL ,
                `fid` INT NOT NULL ,
                `path` TEXT NOT NULL ,
                PRIMARY KEY(`aid`,`fid`)
        ) ENGINE = MYISAM ;
        '''
    execSQL(sql,'FormInfo')
    
def InsertFormInfo(aid,fid,path):
    path = path.replace('\\', '\\\\')
    #path=path.split('\\')
    #path='''{0}\\\{1}\\\{2}'''.format(path[0],path[1],path[2])
    sql='''INSERT INTO `FormInfo`.`Info` 
                (`aid` ,`fid`,`path`) VALUES ('{0}','{1}','{2}') 
                ON DUPLICATE KEY UPDATE `path`='{3}' '''.format(aid,fid,path,path)
    _logger.debug(sql)
    execSQL(sql,'FormInfo')
    

def execSQL(SQL,dbName):
    try:
        conn=MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="password",
                             db=dbName)
        cursor=conn.cursor()
        cursor.execute(SQL)
        cursor.close()
        conn.commit()
        conn.close()
        return True
    except MySQLdb.Error ,e:
        ret="Error %d: %s" % (e.args[0],e.args[1])
        return ret

def main():
    #===========================================================================
    #    All form descriptions will be store in the Schema/{App}/Forms/{*}
    #    The file name is <Form ID>.
    #    This script will take the path to the folder then process all 
    #    form descriptions in the folder
    #    The record in DB is <aid,fid,path>
    #===========================================================================
    createFormInfoDB()
    createFormInfoTable()
    reader=schemaReader()
    path = os.path.abspath(sys.argv[1])
    for f in os.listdir(path):
        fullPath=os.path.join(path,f)
        if fullPath.endswith('xml') or fullPath.endswith('XML'):
            reader.parseFile(fullPath)
            InsertFormInfo(reader.getFormDict()[u'application'],reader.getFormDict()[u'id'],fullPath)
            #print '{0},{1},{2}'.format(reader.getFormDict()[u'application'],
            #reader.getFormDict()[u'id'],fullPath)
    
if __name__ == '__main__':
    main()
