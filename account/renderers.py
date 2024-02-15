from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        respo = renderer_context['response']
        message = renderer_context['response'].headers.get('message')
        status_code = respo.status_code
                
        response = ''
        if 'ErrorDetail' in str(data) or 'non_fields_errors' in str(data):
            response = json.dumps({'success':False,'status':status_code,'message':message,'errors':data})
        else:
            response = json.dumps({'success':True,'status':status_code,'message':message,'data':data})   
             
        return response
    


class CustomJSONRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        respo = renderer_context['response']
        status_code = respo.status_code
        response = ''
        if 'ErrorDetail' in str(data) or 'non_fields_errors' in str(data) or status_code == 404:
            response = json.dumps({'success':False,'status':status_code,'errors':data})
        else:
            response = json.dumps({'success':True,'status':status_code,'data':data})   
             
        return response
    