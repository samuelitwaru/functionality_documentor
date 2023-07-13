from django import  forms
import json

class StringListField(forms.CharField):
    
    def clean(self, value):
        if isinstance(value, list):
            return value
        try:
            return json.loads(value)
        except:
            raise forms.ValidationError(f'Must be list, got {type(value)}')
        

class IntegerMultipleChoiceField(forms.MultipleChoiceField):
    pass
    def clean(self, value):
        # Coerce each selected value to an integer
        return [int(val) for val in value]