from django import forms
from django.forms import ModelForm
from django.forms import modelformset_factory
from django.forms import BaseFormSet
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet
from django.forms import formset_factory
from django.contrib import admin

from .models import (
    Survey,
    Question,
    Option,
    OtherField,
    Vote
)


class CreateSurveyForm(ModelForm):
    survey = forms.CharField(
        required=False,
        label="Namn På Undersökning"
    )

    class Meta:
        model = Survey
        fields = '__all__'
        blank = True
        null = True
        required = False

    def clean(self):
        cleaned_data = super(CreateSurveyForm, self).clean()

        if not self.cleaned_data.get('survey'):
            self.add_error(
                'survey', 'Ange titel på undersökningen'
            )
        elif len(self.cleaned_data.get('survey')) < 5:
            self.add_error(
                'survey', 'För kort titel'
            )
        elif len(self.cleaned_data.get('survey')) > 200:
            self.add_error(
                'survey', 'För lång titel'
            )

        return cleaned_data


class CreateQuestionForm(ModelForm):
    question = forms.CharField(
        required=False,
        label="Namn På Fråga"
    )

    class Meta:
        model = Question
        fields = ('question', 'question_type', 'showOtherField')
        blank = True
        null = True
        required = False

    def clean(self):
        cleaned_data = super(CreateQuestionForm, self).clean()

        if not self.cleaned_data.get('question'):
            self.add_error(
                'question', 'Ange titel på Frågan'
            )
        elif len(self.cleaned_data.get('question')) < 5:
            self.add_error(
                'question', 'För kort fraga'
            )
        elif len(self.cleaned_data.get('question')) > 200:
            self.add_error(
                'question', 'För lang fraga'
            )

        if not self.cleaned_data.get('question_type'):
            self.add_error('question_type', 'Ange typ av Fråga')

        return cleaned_data


CreateOptionFormset = modelformset_factory(
    Option,
    fields=('option', ),
    extra=1
)


class otherForm(ModelForm):
    otherField = forms.CharField(
        label='Other '
    )

    class Meta:
        model = OtherField
        fields = ('otherField', )


class VoteForm(ModelForm):
    # option = forms.ModelChoiceField(
    #     label='OPtion nigger ',
    #     queryset=Option.objects.filter(survey=Survey.objects.get(id=25))
    # )

    class Meta:
        model = Vote
        # fields = ('option', 'question')
        fields = '__all__'

    def clean(self):
        cleaned_data = super(VoteForm, self).clean()
        return cleaned_data


class VoteAdminForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = "__all__"  # for Django 1.8+

    def __init__(self, *args, **kwargs):
        super(VoteAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['option'].queryset = Option.objects.filter(
                survey=Survey.objects.get(id=25))


class VoteAdmin(admin.ModelAdmin):
    form = VoteAdminForm


class BaseVoteFormSet(BaseFormSet):
    def clean(self):
        cleaned_data = super(BaseVoteFormSet, self).clean()
        error_list = []
        for form in self.forms:
            print('##########################')
            print(form.cleaned_data)
            print('##########################')
            if not form.cleaned_data.get('option'):
                error_list.append(ValidationError('Option is fucked'))

            if not form.cleaned_data.get('question'):
                error_list.append(ValidationError('question is fucked'))
                # error_list.append('question')
                # raise ValidationError('question')
                # self.add_error(
                #     'question', 'Ange titel på question'
                # )

                # print(error_list)
                # return error_list
                # if any(self.errors):
                #     return
        if error_list:
            raise ValidationError(error_list)


class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = '__all__'


VoteFormset = formset_factory(
    VoteForm,
    formset=BaseVoteFormSet,
    # fields=('option', 'question'),
    extra=4
)
# VoteFormset = modelformset_factory(
#     Vote,
#     fields=('option', 'question'),
#     extra=4
# )
