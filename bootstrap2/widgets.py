from django.forms.widgets import RadioInput, RadioFieldRenderer, RadioSelect, SelectMultiple, CheckboxInput
from itertools import chain
from django.utils.html import conditional_escape, escape
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe


class OptionsRadioInput(RadioInput):
    def __unicode__(self):
        if 'id' in self.attrs:
            label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = conditional_escape(force_unicode(self.choice_label))
        return mark_safe(u'<label%s>%s <span>%s</span></label>' %
                         (label_for, self.tag(), choice_label))


class OptionsRadioRenderer(RadioFieldRenderer):
    def render(self):
        return mark_safe(u'<ul class="inputs-list">\n%s\n</ul>' %
                         u'\n'.join([u'<li>%s</li>' %
                         force_unicode(w) for w in self]))


class OptionsRadio(RadioSelect):
    renderer = OptionsRadioRenderer

class CheckboxSelectMultiple(SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        global_label = attrs['label'] if attrs and 'label' in attrs else None
        final_attrs = self.build_attrs(attrs, name=name)
        output = []

        output.append(u'<ul class="inputs-list">')
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<li><label%s>%s <span>%s</span></label></li>' % (label_for, rendered_cb, option_label))
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_
    id_for_label = classmethod(id_for_label)