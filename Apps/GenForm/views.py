# Create your views here.
from django.core.context_processors import csrf
from django.http import HttpResponse
from django import template
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

def show_op_form(request):
    if request.method == 'GET' :
        my_csrf = {}
        my_csrf.update(csrf(request))
        app_form_path = 'template/opForm.html'
        return render_to_response (app_form_path, my_csrf)

def gen_op_form(request):
    if request.method == "POST":
        # res = HttpResponse()
        # for data in request.raw_post_data.split("&") :
        #     res.write("<div>{0}</div>".format(data))
        num_of_schemas = 0
        current_schema_id = 0
        form_dict = {}
        data_list = request.raw_post_data.replace('+',' ').split("&")
        csrf_token = data_list.pop(0)
        form_dict['appId'] = data_list.pop(0).split("=")[1]
        form_dict['formId'] = data_list.pop(0).split("=")[1]
        form_dict['formName'] = data_list.pop(0).split("=")[1]
        schemaId = data_list.pop(0).split("=")[1]
        op = data_list.pop(0).split("=")[1]
        if (op == 'Create') : form_dict['opId'] = 0
        elif (op == 'Update') : form_dict['opId'] = 1 
        elif (op == 'Destroy') : form_dict['opId'] = 2
        elif (op == 'Fetch') : form_dict['opId'] = 3
        elif (op == 'Adv Fetch') : form_dict['opId'] = 4
        elif (op == 'Count') : form_dict['opId'] = 5 
        form_dict['schemas'] = []
        while data_list :
            if form_dict['opId'] < 3 :
                current_schema = {'fields':[], 'schemaId':schemaId, }
                num_of_fields = 0
                while data_list :
                    num_of_fields += 1
                    current_schema['fields'].append(
                       {'fieldId':data_list.pop(0).split('=')[1]})
                current_schema['numOfFields'] = num_of_fields
                form_dict['schemas'].append(current_schema)
            elif form_dict['opId'] == 3 or form_dict['opId'] == 5:
                num_of_fields = 0
                num_of_fetch = 0
                current_schema = {'fields':[], 'schemaId':schemaId, 
                   'fetch':[],'logical':'AND', }
                while data_list and not data_list[0].startswith('fetch'):
                    num_of_fields += 1
                    current_schema['fields'].append(
                       {'fieldId':data_list.pop(0).split('=')[1]
                ,'operator':data_list.pop(0).split('=')[1].replace('+',' ')})
                current_schema['numOfFields'] = num_of_fields
                if form_dict['opId'] == 3:
                    while data_list :
                        num_of_fetch += 1
                        current_schema['fetch'].append(
                          data_list.pop(0).split('=')[1])
                    current_schema['numOfFetch'] = num_of_fetch
                form_dict['schemas'].append(current_schema)
        # form_dict = gen_fake_form_dict()        
        doc = render_to_string ('template/form_description.xml', form_dict)
        open("/tmp/{0}.xml".format(form_dict['formName']),"w").write(doc)
        tmp = open('/tmp/{0}.xml'.format(form_dict['formName']),'rb').read()
        res = HttpResponse(tmp, mimetype="application/xml")
        res['Content-Disposition'] = 'attachment; filename={0}.xml'.format( 
                                      form_dict['formName'] )
        return res
    else:
        return HttpResponse("WHF")
def gen_fake_form_dict():
    # This function will return a fake dictionary
    # to present the data.
    # This function is designed to verify app_description.xml
    return { 'appId':'1', 'formName':'fakeformName', 'formId':'1', 'opId':'3',
        'numOfSchemas':'1', 'schemas':[ { 'schemaId':'1', 'numOfFields':'1', 
        'logical':'AND', 'fields': [{'fieldId':'0', 'operator':'Greator Than', }        ],'numOfFetch':'2','fetch':['1', '2', ]}]}
 

