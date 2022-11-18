from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.forms import modelformset_factory
from .forms import (
    CreateSurveyForm,
    CreateQuestionForm,
    CreateOptionFormset,
    VoteFormset,
    otherForm,
    VoteForm,
    VoteAdminForm,

    # VoteFormset
)
from django import forms
from .models import (
    Survey,
    Question,
    Option,
    Vote,


)

# Create your views here.


def home(request):
    surveys = Survey.objects.all()
    surveyForm = CreateSurveyForm(prefix='surveyform')
    if request.method == 'GET':
        surveyForm = CreateSurveyForm(prefix='surveyform')

    if request.method == 'POST':
        surveyForm = CreateSurveyForm(
            request.POST or None, prefix='surveyform')
        if surveyForm.is_valid():
            surveyObj = Survey.objects.create(
                survey=surveyForm.cleaned_data.get('survey')
            )
            return redirect('createSurvey', pk=surveyObj.id)

    context = {
        'surveys': surveys,
        'surveyForm': surveyForm
    }

    return render(request, 'base/home.html', context)


def createSurvey(request, pk, *args, **kwargs):
    print('Survey PK: ', pk)

    if request.method == 'GET':

        survey = Survey.objects.get(id=pk)
        surveyForm = CreateSurveyForm(
            instance=Survey.objects.get(id=pk), prefix='createSurvey')
        questionForm = CreateQuestionForm(request.GET or None)
        optionFormset = CreateOptionFormset(queryset=Option.objects.none())
        theOtherForm = otherForm(request.GET or None, prefix='otherForm')

        context = {
            'survey': survey,
            'surveyForm': surveyForm,
            'questionForm': questionForm,
            'optionFormset': optionFormset,
            'otherForm': theOtherForm

        }

    if request.method == 'POST':
        print(request.POST)

        if 'createSurvey-survey' in request.POST:

            surveyForm = CreateSurveyForm(request.POST, prefix='createSurvey')

            if surveyForm.is_valid():

                surveyObj = Survey.objects.get(id=pk)
                surveyObj.survey = surveyForm.cleaned_data.get('survey')
                surveyObj.save()

                return JsonResponse({'survey': surveyObj.survey}, status=201)
            else:
                print('####################################')
                print(surveyForm.errors)
                for x in surveyForm.errors:
                    print('error ', x)

                print('####################################')
                return JsonResponse({'errorList': surveyForm.errors}, status=201)

        elif 'question' in request.POST:
            print('####################################')
            print('question: ', request.POST.get('question'))
            print('question_type: ', request.POST.get('question_type'))
            print('Show Other Field: ', request.POST.get('showOtherField'))
            print('####################################')

            questionForm = CreateQuestionForm(request.POST)
            optionFormset = CreateOptionFormset(request.POST, request.FILES)

            if questionForm.is_valid():
                print('Qurstion is valid')
            if optionFormset.is_valid():
                print('optionFormset is valid')

            if all([questionForm.is_valid(), optionFormset.is_valid()]):
                print('Everyting is valid')
                print(optionFormset.cleaned_data)

                surveyObj = Survey.objects.get(id=pk)

                questionObj = Question.objects.create(
                    question=questionForm.cleaned_data.get('question'),
                    survey=surveyObj,
                    question_type=questionForm.cleaned_data.get(
                        'question_type'),
                    showOtherField=questionForm.cleaned_data.get(
                        'showOtherField'),
                )

                optionDict = dict()
                for option in optionFormset:
                    if option.cleaned_data.get('option'):
                        optionObj = Option.objects.create(
                            option=option.cleaned_data.get('option'),
                            question=questionObj,
                            survey=surveyObj
                        )
                        optionDict[optionObj.option] = optionObj.id
                return JsonResponse({
                    # 'survey': surveyForm.cleaned_data.get('survey'),
                    'question': questionForm.cleaned_data.get('question'),
                    'questionId': questionObj.id,
                    'optionDict': optionDict,
                    'showOtherForm': questionForm.cleaned_data.get('showOtherField'),
                    'questionType': questionForm.cleaned_data.get('question_type'),
                }, status=201)
            else:
                allErrors = dict()
                # if surveyForm.errors:
                #     allErrors['surveyFormErrors'] = surveyForm.errors
                if questionForm.errors:

                    # allErrors.update({'questionErrors': questionForm.errors.as_json()})
                    allErrors['questionErrors'] = questionForm.errors.as_json()
                    for x in questionForm.errors.as_data().values():
                        print(x[0])
                        print(type(x[0]))
                    # allErrors.append(questionForm.errors.as_json())
                    # allErrors.append(questionForm.errors.as_json())

                if optionFormset.errors:
                    print(optionFormset.errors)
                    # allErrors['optionErrors'] = optionFormset.errors
                    # allErrors.append(optionFormset.errors.as_json())

                return JsonResponse({'errors': [(k, v[0]) for k, v in questionForm.errors.items()]}, safe=False, status=200)

        elif 'deletequestionId' in request.POST:

            if Question.objects.filter(id=request.POST.get('deletequestionId')).exists():
                questionObj = Question.objects.get(
                    id=request.POST.get('deletequestionId'))
                surveyObj = Survey.objects.get(id=pk)
                if questionObj.survey == surveyObj:
                    questionObj.delete()
                    return JsonResponse({'success': 'succes muther'}, status=201)
            else:
                return JsonResponse({'error': 'Frågan matchar inte Undersökningen'}, status=201)

        elif 'previewQuestionId' in request.POST:
            # ! I dont use this???
            print('######################################')
            print(request.POST)

            questionId = request.POST.get('previewQuestionId')
            optionId = request.POST.get('previewOptionId')

            if not Option.objects.filter(id=optionId).exists():
                return JsonResponse({'failure': 'Alternativet finns inte'}, status=200)
            elif not Question.objects.filter(id=questionId):
                return JsonResponse({'failure': 'Frågan finns inte'}, status=200)
            else:

                optionObj = Option.objects.get(id=optionId)
                questionObj = Question.objects.get(id=questionId)

                if not questionObj.option_set.all().count() > 1:
                    return JsonResponse({'failure': 'Frågan måste ha minst ett allternativ'}, status=200)

                if optionObj.question == questionObj:
                    optionObj.delete()
                    return JsonResponse({'success': 'succes muther'}, status=201)
                else:
                    return JsonResponse({'failure': 'Allternativet matchar inte med frågan'}, status=200)

        elif 'addPreviewOption' in request.POST:

            if 'optionId' in request.POST:
                print('passed 1')
                if Question.objects.get(id=request.POST.get('questionId')):
                    print('passed 2')
                    questionObj = Question.objects.get(
                        id=request.POST.get('questionId'))
                    if questionObj.survey == Survey.objects.get(id=pk):
                        print('passed 3')

                        if Option.objects.get(id=request.POST.get('optionId')).question == questionObj:
                            print('passed 4')
                            optionObj = Option.objects.get(
                                id=request.POST.get('optionId'))
                            optionObj.option = request.POST.get(
                                'addPreviewOption')
                            optionObj.save()
                            return JsonResponse({'success': 'Frågan och allternativet matchar inte'}, status=201)

                        else:
                            return JsonResponse({'error': 'Frågan och allternativet matchar inte'}, status=201)

                    else:
                        return JsonResponse({'error': 'Frågan och undersökningen matchar inte'}, status=201)

                else:
                    return JsonResponse({'error': 'Frågan finns inte'}, status=201)

            else:
                if Question.objects.get(id=request.POST.get('questionId')):
                    questionObj = Question.objects.get(
                        id=request.POST.get('questionId'))

                    if questionObj.survey == Survey.objects.get(id=pk):
                        questionId = int(request.POST.get('questionId'))
                        optionTest = request.POST.get('addPreviewOption')
                        optionObj = Option.objects.create(
                            option=optionTest,
                            question=Question.objects.get(id=questionId),
                            survey=Survey.objects.get(id=pk)
                        )
                        return JsonResponse({'dataId': optionObj.id}, status=200)
                    else:
                        return JsonResponse({'error': 'Frågan och undersökningen matchar inte'}, status=201)

                else:
                    return JsonResponse({'error': 'Frågan finns inte'}, status=201)

        elif 'DeleteottherFieldQuestionId' in request.POST:
            print('delete other field')
            if Question.objects.filter(id=request.POST.get('DeleteottherFieldQuestionId')).exists():
                print('check 1')
                questionObj = Question.objects.get(
                    id=request.POST.get('DeleteottherFieldQuestionId'))
                if questionObj.survey == Survey.objects.get(id=pk):
                    print('check 2')
                    questionId = request.POST.get(
                        'DeleteottherFieldQuestionId')
                    questionObj = Question.objects.get(id=questionId)
                    questionObj.showOtherField = False
                    questionObj.save()
                    return JsonResponse({'success': 'success'}, status=200)
                else:
                    return JsonResponse({'error': 'Fråga matchar inte undersökning'}, status=200)
            else:
                return JsonResponse({'error': 'Fråga existerar inte'}, status=200)

        elif 'addOtherFieldId' in request.POST:
            print('##########')
            print(request.POST)
            print('the fuck nigga?')
            if Question.objects.filter(id=request.POST.get('addOtherFieldId')).exists():
                questionObj = Question.objects.get(
                    id=request.POST.get('addOtherFieldId'))
                if questionObj.survey == Survey.objects.get(id=pk):
                    questionObj.showOtherField = True
                    questionObj.save()
                    return JsonResponse({'success': 'success'}, status=200)
                else:
                    return JsonResponse({'error': 'Frågan matchar inte undersökningen'}, status=200)
            else:
                return JsonResponse({'error': 'Frågan finns inte'}, status=200)

        elif 'questionPreviewTitle' in request.POST:
            print('#################')
            print(request.POST)
            print(request.POST.get('questionPreviewTitleId'))
            if Question.objects.filter(id=request.POST.get('questionPreviewTitleId')).exists():
                questionObj = Question.objects.get(
                    id=request.POST.get('questionPreviewTitleId'))
                if questionObj.survey == Survey.objects.get(id=pk):

                    questionObj.question = request.POST.get(
                        'questionPreviewTitle')
                    questionObj.save()
                    return JsonResponse({'success': 'success'}, status=200)
                else:
                    return JsonResponse({'error': 'Frågan matchar inte undersökningen'}, status=200)
            else:
                return JsonResponse({'error': 'Frågan finns inte'}, status=200)

        elif 'select' in request.POST:
            if Question.objects.filter(id=request.POST.get('selectQuestion')).exists():
                questionObj = Question.objects.get(
                    id=request.POST.get('selectQuestion'))
                if questionObj.survey == Survey.objects.get(id=pk):
                    if request.POST.get('questionPreviewTitle') == 'radio' or request.POST.get('questionPreviewTitle') == 'checkbox':
                        questionObj.question_type = request.POST.get('select')
                        questionObj.save()
                        return JsonResponse({'success': 'success'}, status=200)
                else:
                    return JsonResponse({'error': 'Frågan matchar inte undersökningen'}, status=200)
            else:
                return JsonResponse({'error': 'Frågan finns inte'}, status=200)

    return render(request, 'base/createsurvey.html', context)

#  Option.objects.filter(survey=Survey.objects.get(id=25))


def takeSurvey(request, pk):
    survey = Survey.objects.get(id=pk)

    if request.method == 'GET':
        option = [Option.objects.all()]

        theOtherForm = otherForm(prefix='otherForm')

        # voteformset = VoteFormset(queryset=Vote.objects.none(), prefix='voteFormset')
        voteformset = VoteFormset(prefix='voteFormset')
        context = {
            'survey': survey,
            'otherForm': theOtherForm,
            'voteFormset': voteformset,

        }

        return render(request, 'base/takesurvey.html', context)

    if request.method == 'POST':
        print('post')
        # print(request.POST)

        surveyObj = Survey.objects.get(id=pk)
        voteformset = VoteFormset(request.POST, prefix='voteFormset')

        # print(voteformset)

        # for f in voteformset:
        #     print(f)
        #     if f.is_valid():
        #         print('valid')
        # return JsonResponse({'error': 'error'}, status=200)

        if voteformset.is_valid():
            print(voteformset.non_form_errors(),
                  '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            isReallyValid = True
            print('#################################################valid#################################################')

            for voteform in voteformset:
                if not voteform.cleaned_data.get('option'):
                    isReallyValid = False
                    break
                if not voteform.cleaned_data.get('question'):
                    isReallyValid = False
                    break
            if isReallyValid:
                for voteform in voteformset:

                    Vote.objects.create(
                        survey=surveyObj,
                        vote=True,
                        option=voteform.cleaned_data.get('option'),
                        question=voteform.cleaned_data.get('question')
                    )
                    print('##########################################################')
                    print(voteform.cleaned_data.get('option'))
                    print(voteform.cleaned_data.get('question'))
                    print('##########################################################')
                return JsonResponse({'success': 'success'}, status=200)
            else:
                return JsonResponse({'sorta': 'no created empty form'}, status=200)

        else:
            print(voteformset.non_form_errors(),
                  '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # print(voteformset.errors(), '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # print('errors: ', dict(voteformset.errors))
            # return JsonResponse({'error': dict(voteformset.errors.items())}, status=200)
            return JsonResponse({'error': 'error'}, status=200)

# JSON 201 => OK and created object
# JSON 20 => OK, but did not create object


def newQuestion(request):
    if request.method == 'GET':
        questionForm = CreateQuestionForm(
            request.GET or None, prefix='questionForm')
        optionFormset = CreateOptionFormset(
            queryset=Option.objects.none(), prefix='optionFormset')
        context = {
            'questionForm': questionForm,
            'optionFormset': optionFormset,
        }
        return render(request, 'base/createquestion.html', context)
    if request.method == 'POST':

        questionForm = CreateQuestionForm(request.POST, prefix='questionForm')
        optionFormset = CreateOptionFormset(
            request.POST, request.FILES, prefix='optionFormset')
        # print(optionFormset)
        for form in optionFormset:
            print(form)
        if questionForm.is_valid():
            print('Qurstion is valid', questionForm.cleaned_data)

        if optionFormset.is_valid():
            print('optionFormset is valid', optionFormset.cleaned_data)
    return JsonResponse({'lefig': 'lefit'})
