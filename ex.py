from django.template.defaultfilters import safe
from core.models import Functionality
import json

def convert_text_to_quill_html(text_value):

    # Convert newlines to <br> tags to maintain line breaks
    text_with_br = text_value.replace('\n', '<br>')
    
    # Wrap the content with the Quill editor's container class
    quill_html = f'<div class="ql-editor">{text_with_br}</div>'
    
    # Mark the string as safe to prevent auto-escaping in templates
    return json.dumps({
        'delta': '',
        'html': safe(quill_html)
    })

objs = Functionality.objects.all()

for obj in objs:
    print(obj)
    obj.description = convert_text_to_quill_html(obj.description)
    print(obj.description)
    obj.save()