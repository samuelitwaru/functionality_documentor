from django import  forms
import json

class StringListField(forms.CharField):
    
    def clean(self, value):
        print('>>>>>.', value)
        if isinstance(value, list):
            return value
        try:
            return json.loads(value)
        except:
            raise forms.ValidationError(f'Must be list, got {type(value)}')