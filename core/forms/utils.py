from django import  forms
import json

class StringListField(forms.CharField):
    
    def clean(self, value):
        if isinstance(value, list):
            return value
        try:
            return json.loads(value)
        except:
            raise forms.ValidationError