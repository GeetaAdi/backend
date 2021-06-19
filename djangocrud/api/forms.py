from django import forms
from django.core.exceptions import ValidationError

FRUIT_CHOICES= [
    ('1', 'Cultural Destructiveness (See the difference; stomp it out.)'),
    ('2', 'Cultural Incapacity (See the difference; make it wrong.)'),
    ('3', 'Cultural Blindness (See the difference; dismiss it.)'),
    ('4', 'Cultural Pre-Competence (See the difference; recognize what you don’t know.)'),
    ('5', 'Cultural Competence (See the difference; understand the difference that difference makes.)'),
    ('6', 'Cultural Proficiency (See the difference; respond positively and affirmingly.)'),
    ]

class MultipleValueWidget(forms.TextInput):
    def value_from_datadict(self, data, files, name):
        return data.getlist(name)

class MultipleValueRadioWidget(forms.RadioSelect):
    def __init__(self, *args, **kwargs):
        self.choices = FRUIT_CHOICES
    def value_from_datadict(self, data, name):
        return data.getlist(name)

class MultipleValueField(forms.Field):
    widget = MultipleValueWidget


class MultipleValueRadioField(forms.Field):
    widget = MultipleValueRadioWidget


def clean_int(x):
    try:
        return int(x)
    except ValueError:
        raise ValidationError("Cannot convert to integer: {}".format(repr(x)))


class MultipleIntField(MultipleValueField):
    def clean(self, value):
        return [clean_int(x) for x in value]

class MultipleStringField(MultipleValueField):
    def clean(self, value):
        return [x for x in value]

class MultipleRadioField(MultipleValueRadioField):
    def clean(self, value):
        return [x for x in value]


# class HorizontalRadioRenderer(forms.RadioSelect.renderer):
#   def render(self):
#     return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class ScoreForm(forms.Form):
    # score = MultipleIntField()
    Comments_For_Participant = MultipleStringField()
    Comments_For_Facilitator = MultipleStringField()
    # score = MultipleIntField()

class RadioForm1(forms.Form):
    score1 = forms.ChoiceField(choices=FRUIT_CHOICES, widget=forms.RadioSelect)

class RadioForm2(forms.Form):
    score2 = forms.ChoiceField(choices=FRUIT_CHOICES, widget=forms.RadioSelect)

class RadioForm3(forms.Form):
    score3 = forms.ChoiceField(choices=FRUIT_CHOICES, widget=forms.RadioSelect)

class RadioForm4(forms.Form):
    score4 = forms.ChoiceField(choices=FRUIT_CHOICES, widget=forms.RadioSelect)