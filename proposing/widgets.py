from django.forms import widgets
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.encoding import force_unicode

class TagSelectorWidget(widgets.SelectMultiple):

    class Media:
        css = {
            'all': ('css/chosen/chosen.css',)
        }
        js = ('js/chosen/chosen.jquery.js',)

    def render(self, name, selected=None, attrs=None, choices=()):
        if selected is None: selected = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select multiple="multiple" class="chosen" %s>' % flatatt(final_attrs)]
        options = self.render_options(choices, selected)
        if options:
            output.append(options)
        output.append('</select>')
        output.append('<script type="text/javascript">$("#%s").chosen({width: "100%%"});</script>'%attrs['id'])
        return mark_safe(u'\n'.join(output))



class RichTextEditorWidget(widgets.Textarea):

    class Media:
        css = {
            'all': ('css/wysihtml5/bootstrap-wysihtml5.css',)#comma is important!
        }
        js = ('js/wysihtml5/wysihtml5-0.3.0.js',
              'js/wysihtml5/bootstrap-wysihtml5.js')

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        del final_attrs['rows']
        del final_attrs['cols']
        output = [u'<textarea class="rich-text-widget" %s>' % flatatt(final_attrs)]
        output.append('%s'%value)
        output.append('</textarea>')
        output.append("""<script type="text/javascript">$('#%s').wysihtml5({
            "font-styles": true,
            "emphasis": true,
            "lists": true,
            "html": false,
            "link": true,
            "image": false,
            "color": false  
        });</script>"""%attrs['id'])
        return mark_safe(u'\n'.join(output))

class VeryRichTextEditorWidget(widgets.Textarea):
    class Media:
        css = {
            'all': ('lib/x-editable/bootstrap-editable/css/bootstrap-editable.css',
                    'css/wysihtml5/bootstrap-wysihtml5.css')
        }
        js = ('lib/x-editable/bootstrap-editable/js/bootstrap-editable.js',
              'js/wysihtml5/wysihtml5-0.3.0.js',
              'js/wysihtml5/bootstrap-wysihtml5.js')
        

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<div id="username" %s>%s</div>' % (flatatt(final_attrs), value)]
        output.append("""
        <script type="text/javascript">
            $.fn.editable.defaults.mode = 'inline';
            $(document).ready(function() {
                $('#username').editable({
                    type: 'wysihtml5',
                    pk: '%s',
                    url: '/post',
                    title: 'Enter your proposal',
                    success: function(response, newValue) {
                        if(response.status == 'error') return response.msg; //msg will be shown in editable form
                    },
                    anim: "fast"
                });
            });
        </script>"""%attrs['id'])
        return mark_safe(u'\n'.join(output))
