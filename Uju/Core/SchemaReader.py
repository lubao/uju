'''
Created on Oct 19, 2009

@author: paul
'''
from xml.sax.handler import ContentHandler
from xml.sax import parse
from SQLEng import SQLEng
from copy import copy
import os
import Defines

class AppReader():
    '''
    classdocs
    This class is called whenever SMSAppStore
    needs to know the application description
    '''
    def parse_file(self,id):
        my_Handler  =  AppHandler()
        my_SQL = SQLEng()
        path = my_SQL.getAppPath(id)
        path = os.path.join(Defines.PATHPREFIX,path[0][0])
        with open("{0}".format(path),'r') as f:
            parse(f,my_Handler)
            f.close()
        
        return my_Handler.app_dict

class FormReader():
    '''
    classdocs
    This class is called whenever SMSAppStore
    needs to know the form description
    '''
    def parse_file(self,aid,fid):
        my_Handler = FormHandler()
        my_SQL = SQLEng()
        path = my_SQL.getFormPath(aid,fid)
        path = os.path.join(Defines.PATHPREFIX,path[0][0])
        with open("{0}".format(path),'r') as f:
            parse(f,my_Handler)
            f.close()
        return my_Handler.form_dict
    
class AppHandler(ContentHandler):
    
    def __init__(self):
        self.app_dict = {}
        self.schemas_dict = {}
        self.fields_dict = {}
        self.app_dict['schemas'] = self.schemas_dict
        self.current_schema_id = 0
        self.current_schema_name=''
        self.current_field_id = 0

    def startElement(self,name,attrs): 
        if name == 'application': 
            nameList = attrs.getNames()
            for i in range(len(nameList)):
                self.app_dict[nameList[i]] = attrs.getValue(nameList[i])
        if name == 'schema':
            self.current_schema_id = attrs.getValue('id')
            self.current_schema_name = attrs.getValue('name')
        if name == 'field':
            field = {}
            field['name'] = attrs.getValue('name')
            field['range'] = attrs.getValue('range')
            self.fields_dict[attrs.getValue('id')] = field
            self.current_field_id = attrs.getValue('id')
        if name == 'choice':
            field = self.fields_dict[self.current_field_id]
            if 'choice' in field:
                chList = field['choice']
                chList.append(attrs.getValue('name'))
                self.fields_dict[self.current_field_id] = field
            else:
                chList = [attrs.getValue('name')]
                field['choice'] = chList
                self.fields_dict[self.current_field_id] = field
    
    def endElement(self,name):
        if name == 'schema': 
            self.fields_dict['name'] = self.current_schema_name
            self.schemas_dict[self.current_schema_id] = self.fields_dict.copy()
            self.fields_dict.clear()
            
class FormHandler(ContentHandler):
    def __init__(self):
        self.form_dict = {}
        self.schemas_dict = {}
        self.fields_dict = {}
        self.fields_list = []
        self.fetch_list = []
        self.fields_dict['fields'] = self.fields_list
        self.fields_dict['fetch'] = self.fetch_list
        self.form_dict['schemas'] = self.schemas_dict
        self.isFetch = False
        self.current_schema_id = 0
    
    def startElement(self,name,attrs): 
        if name == 'form': 
            nameList = attrs.getNames()
            for i in range(len(nameList)):
                self.form_dict[nameList[i]] = attrs.getValue(nameList[i])
        if name == 'schema':
            self.current_schema_id = attrs.getValue('id')
            self.fields_list = []
            self.fetch_list = []
            self.fields_dict.clear()
            self.fields_dict['fields'] = self.fields_list
            self.fields_dict['fetch'] = self.fetch_list
        if name == 'field':
            if not self.isFetch:
                self.fields_list.append(attrs.getValue('id'))
            else:
                self.fetch_list.append(attrs.getValue('id'))
        if name == 'fetch':
            self.isFetch = True
    
    def endElement(self,name):
        if name == 'schema': 
            self.schemas_dict[self.current_schema_id] = copy(self.fields_dict)
