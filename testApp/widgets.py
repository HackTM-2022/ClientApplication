from django.forms import DateInput,FileInput,ClearableFileInput, CheckboxInput
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils import dateformat
from django.conf import settings

class FengyuanChenDatePickerInput(DateInput):
    template_name = 'widgets/datepicker_widget.html'
    def format_value(self, value):
        try:
            return dateformat.format(value, settings.MY_DATE_FORMAT)
        except:
            return "01/01/2022"

class CustomFileWidget(ClearableFileInput):
    def __init__(self, attrs={}):
        super(CustomFileWidget, self).__init__(attrs)

    template_with_initial = u'<input type="file" name="%(name)s" id="id_%(name)s" tabindex="-1" style="position: absolute; clip: rect(0px, 0px, 0px, 0px);">\
         <div class="current-file-text">Current file</div>%(initial)s <br/>  %(clear_template)s<br />'
    template_with_clear = '%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    def render(self, name, value, attrs=None, renderer=None):
        substitutions = {
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(CustomFileWidget, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = (u'<a class="current-file-link" target="_blank" href="%s">%s</a>'
                                        % (escape(value.url), value.url.split("/")[len(value.url.split("/"))-1]))
            substitutions['name'] = name
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)