from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        message = renderer_context['response'].headers.get('message')
        response = ''
        if 'ErrorDetail' in str(data) or 'non_fields_errors' in str(data):
            response = json.dumps({'success':False,'message':message,'errors':data})
        else:
            response = json.dumps({'success':True,'message':message,'data':data})   
             
        return response