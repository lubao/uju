#!/usr/bin/env python
import MySQLdb,sys,os,string
from xml.sax.handler import ContentHandler
from xml.sax import parse
import logging
import os
from django.db import models
from django.db import connection
from django.contrib import databrowse
from django.core.management import execute_from_command_line
class AppHandler(ContentHandler):
    '''
    A XML Content Handler class for application description
    '''
    global app_dict,schemas_dict,fields_dict,current_schema_id
    global current_field_id,current_schema_name
    
    def __init__(self):
        self.app_dict={}
        self.schemas_dict={}
        self.fields_dict={}
        self.app_dict['schemas']=self.schemas_dict
    
    def startElement(self,name,attrs): 
        if name=='application': 
            name_list=attrs.getNames()
            for i in range(len(name_list)):
                self.app_dict[name_list[i]]=attrs.getValue(name_list[i])
        '''
        app_dict is a Dictionary which holds the attributes of application
        '''
        if name=='schema':
            self.current_schema_id=attrs.getValue('id')
            self.current_schema_name=attrs.getValue('name')
        
        if name=='field':
            field={}
            field['name']=attrs.getValue('name')
            field['range']=attrs.getValue('range')
            self.fields_dict[attrs.getValue('id')]=field
            self.current_field_id=attrs.getValue('id')
            '''
            field id will be the key of the fields_dict.
            name and range of the field are the value of the key
            '''
        
        if name=='choice':
            '''
            Each choice will runs into this function
            Thus, the field may have choices or 
            this is the first choice.
            '''
            field=self.fields_dict[self.current_field_id]
            
            if 'choice' in field:
                choice_list=field['choice']
                choice_list.append(attrs.getValue('name'))
                self.fields_dict[self.current_field_id]=field
                '''
                Choice is a LIST in the field dictionary
                '''
            else:
                choice_list=[attrs.getValue('name')]
                field['choice']=choice_list
                self.fields_dict[self.current_field_id]=field
    
    def endElement(self,name):
        '''
        Here is the end of a schema.
        '''
        if name=='schema': 
            self.fields_dict['name']=self.current_schema_name
            self.schemas_dict[self.current_schema_id]=self.fields_dict.copy()
            self.fields_dict.clear()


class SchemaReader():
    '''
    A XML reader classs
    '''
    global my_handler

    def parse_file(self,path):
        self.my_handler=AppHandler()
        with open("{0}".format(path),'r') as f:
            parse(f,self.my_handler)
        f.close()

    def get_app_dict(self):
        return self.my_handler.app_dict


def create_model(name, fields=None, app_label='', module='', 
		options=None, admin_opts=None
    ):
    """
    Create specified model
    """
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass
        for key, value in admin_opts:
            setattr(Admin, key, value)
        admin.site.register(model, Admin)

    return model

def create_table(app_name,schema_dict):
    schema_name=schema_dict.pop('name')
    sql='''
        CREATE TABLE `{0}_{1}` (
        `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        '''.format(app_name,schema_name)
    model_fields = {'id':models.AutoField(primary_key=True)}
    #model_fields = []
    for i in range(len(schema_dict)):
        # String type
        name = schema_dict[str(i)]['name'].replace(' ','_')
        if schema_dict[str(i)]['range']=='0':
            sql="{0}{1}".format(
                sql,"`{0}` TEXT NULL,".format(name)
            )
            model_fields[name] = models.TextField(db_column=name)
            #model_fields.append(
            #    '\t{0}={1}'.format(name,'models.TextField()')
            #)
        else:
            sql="{0}{1}".format(
                sql,"`{0}` INT NULL,".format(name)
            )
            model_fields[name] = models.IntegerField(db_column=name)
            #model_fields.append(
            #    '\t{0}={1}'.format(name,'models.IntegerField()')
            #)
    sql='''{0} `Time` TIMESTAMP NOT NULL ) ENGINE = MYISAM ;'''.format(sql)
    model_fields['Time']=models.DateTimeField(auto_now=True, db_column='Time')
    #model_fields.append(
    #    '\t{0}={1}'.format('Time','models.DateTimeField(auto_now=True)')
    #)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
    except MySQLdb.Error, e:
        pass
    #models.write('class {0}_{1} (models.Model):\n'.format(app_name,name))
    #models.write('\n'.join(model_fields))
    #models.write('\n\n')
    #databrowse.site.register(
    #        '{0}.{1}.{2}_{3}'.format('Apps', 'DynamicModels', app_name, name)
    #)
    return create_model(
                name='{0}.{1}'.format(app_name, schema_name),
                app_label='Apps',
                fields=model_fields,
                module=app_name,
                options={'db_table':'{0}_{1}'.format(app_name, schema_name)}
            )


PATH = os.getcwd() + '/Apps/Schema'
#models = open(os.getcwd() + '/Apps/DynamicModels.py','w')
schema_reader = SchemaReader()
apps_directory = os.listdir(PATH)
for app in apps_directory:
    schema_reader.parse_file(
        PATH+'/{0}/application_description.xml'.format(app)
    )
    app_dict = schema_reader.get_app_dict()
    for schema in app_dict[u'schemas'].itervalues():
    	try:
            databrowse.site.register(
                create_table(app_name=app_dict[u'name'], schema_dict=schema)
            )
        except:
            pass

