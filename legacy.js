
    let windowUrl = window.location.href;
    let idNum = windowUrl.split('/').slice(-1)[0];
    let url = "{% url 'createSurvey' 0 %}".replace('0', idNum)
    let form = document.querySelector('#form');
    let surveyForm = document.querySelector('#surveyForm');
    let surveyFormInput = document.querySelector('#id_surveyForm-survey');
    let h1 = document.querySelector('h1');
    // let other = document.querySelector('#id_otherField').parentElement;
    let giveOtherField = false;
    let showOtherFieldCheck = document.querySelector('#id_showOtherField');
    showOtherFieldCheck.addEventListener('click', showOtherForm)

    document.querySelector('.otherField').querySelector('input').disabled = true;

    Array.from(document.querySelectorAll('.previewOtherField')).forEach(element => {
        element.querySelector('input').disabled = true;
    });

    function showOtherForm() {

        let otherField = document.querySelector('.otherField');
        otherField.classList.toggle('hide');
        console.log('###############################')
        console.log(otherField.classList)
        console.log('###############################')
    }

    let previewAddOtherFieldBtns = Array.from(document.querySelectorAll('.previewAddOtherFieldBtn'))

    previewAddOtherFieldBtns.forEach(btn => {
        console.log('add option field')
        btn.addEventListener('click', () => {
            addPreviewOtherField(btn)
        })
    })

    function addPreviewOtherField(element) {

        let questionId = element.parentElement.getAttribute('data-id')
        let question = element.parentElement
        console.log(questionId)
        formData = new FormData
        formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
        formData.append('addOtherFieldId', questionId)
        fetch(url, {
            method: 'POST',
            body: formData
        })

            .then(response => response.json())
            .then(data => {
                console.log(data)
                let previewOtherField = document.createElement('div')
                previewOtherField.setAttribute('class', 'previewOtherField')
                let previewOtherFieldInput = document.createElement('input');
                previewOtherFieldInput.setAttribute('type', 'text')
                previewOtherField.appendChild(previewOtherFieldInput);



                let previewOtherFieldBtn = document.createElement('button');
                previewOtherFieldBtn.setAttribute('type', 'button');
                previewOtherFieldBtn.setAttribute('class', 'previewOtherFieldBtn');



                previewOtherFieldBtn.addEventListener('click', () => {
                    deletePreviewOtherField(previewOtherFieldBtn)
                })


                previewOtherFieldBtn.textContent = 'Delete'
                previewOtherField.appendChild(previewOtherFieldBtn);

                let insertbefore = question.querySelector('.previewAllOptionsContainer')
                console.log(insertbefore)
                insertbefore.insertBefore(previewOtherField, null)

            })
            .catch(error => {
                console.log(error, 'error')

            })
    }


    surveyFormInput.addEventListener('focusout', submitSurvey)
    surveyFormInput.addEventListener('input', updateSurveyH1)


    surveyForm.addEventListener('onfocusout', (e) => {
        e.preventDefault()
        submitSurvey()

    })

    let previewAddBtns = Array.from(document.querySelectorAll('.previewAddBtn'));
    previewAddBtns.forEach(element => {
        element.addEventListener('click', () => {
            addPreviewOption(element);
        })
    })

    let deleteBtns = Array.from(document.querySelectorAll('.deleteBtn'))
    deleteBtns.forEach(element => {
        element.addEventListener('click', () => {
            deletePreview(element.parentElement)
        })
    })

    let previewDeleteBtns = Array.from(document.querySelectorAll('.previewDeleteBtn'))
    previewDeleteBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            deletePreviewOption(btn)
        })
    })

    let previewOtherFieldBtns = Array.from(document.querySelectorAll('.previewOtherFieldBtn'))
    previewOtherFieldBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            deletePreviewOtherField(btn)
        })
    })

    function deletePreviewOtherField(element) {
        // element.parentElement.remove()
        let otherField = element.parentElement
        let question = element.parentElement.parentElement
        let questionId = question.getAttribute('data-id')
        console.log(questionId)

        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
        formData.append('deletePreviewOtherFieldQuestionId', questionId)

        fetch(url, {
            method: 'POST',
            body: formData,
        })

            .then(respnse => respnse.json())
            .then(data => {
                
                // otherField.remove()
                let previewAddOtherFieldBtn = document.createElement('button')
                previewAddOtherFieldBtn.setAttribute('class', 'previewAddOtherFieldBtn')
                previewAddOtherFieldBtn.textContent = 'Add other field';
                previewAddOtherFieldBtn.addEventListener('click', () => {
                    addPreviewOtherField(previewAddOtherFieldBtn)
                })

               
                question.replaceChild(previewAddOtherFieldBtn, otherField)
                console.log(data, 'data')
            })

            .catch(error => {
                console.log(error, 'errror')
            })

    }


    function deletePreviewOption(element) {
        console.log('####################################')

        let optionId = element.parentElement.getAttribute('data-id')
        let question = element.parentElement.parentElement.parentElement;
        option = element.parentElement
        let questionId = question.getAttribute('data-id')


        console.log(optionId, 'optionId')
        console.log(questionId, 'questionId')
        console.log(element, 'element')

        console.log('####################################')

        let formdata = new FormData()
        formdata.append('csrfmiddlewaretoken', '{{ csrf_token }}');
        formdata.append('previewQuestionId', questionId)
        formdata.append('previewOptionId', optionId)


        if (Array.from(question.querySelectorAll('.previewOptionContainer')).length > 1) {
            fetch(url, {
                method: 'POST',
                body: formdata
            })
                .then(response => response.json())
                .then(data => {


                    if (data.success) {
                        option.remove()

                        if (Array.from(question.querySelectorAll('.previewOptionContainer')).length == 1) {

                            question.querySelector('.previewOptionContainer').querySelector('button').remove()

                        }


                    }
                    if (data.failure) {
                        let error = document.createElement('p')
                        question.querySelector('.previewError').textContent = data.failure;

                    }
                })

                .catch((error) => {
                    console.log('errro', error)
                })

        }

    }

    function updateSurveyH1() {
        h1.textContent = surveyFormInput.value;
    }

    function submitSurvey() {

        let surveyFormData = new FormData(surveyForm);
        fetch(url, {
            method: 'POST',
            body: surveyFormData,
        })
            .then(response => response.json())
            .then(data => {

                h1.textContent = `${data.survey}`;
            })

            .catch((error) => {
                console.log('error', error);
            })


    }


    addBtn.addEventListener('click', addOption)

    let removeBtns = Array.from(document.querySelectorAll('.removeBtn'));
    removeBtns.forEach(element => {

        element.addEventListener('click', () => {

            removeOption(element)
        })
    });

    function updateBtnList(element) {
        let removeBtns = Array.from(document.querySelectorAll('.removeBtn'));

        element.addEventListener('click', () => {
            removeOption(element)
        })

    }


    function removeOption(element) {
        let allOptions = Array.from(document.querySelectorAll('.optionContainer'));
        if (allOptions.length > 1) {
            let parent = element.parentElement.parentElement;

            let index = allOptions.indexOf(parent) + 1
            for (i = index; i < allOptions.length; i++) {

                let counter = i - 1

                let option = allOptions[i]

                let label = option.querySelector('label');

                label.setAttribute('for', `id_form-${counter}-option`)

                let Input = option.querySelector('input');
                Input.setAttribute('id', `id_form-${counter}-option`)
                Input.setAttribute('name', `form-${counter}-option`)

                let HiddenInput = option.querySelectorAll('input')[1];

                HiddenInput.setAttribute('id', `id_form-${counter}-id`)
                HiddenInput.setAttribute('name', `form-${counter}-id`)

                let allOptionsContainer = document.querySelector('.allOptionsContainer');

            }
            parent.remove()

            let totalForms = document.querySelector('#id_form-TOTAL_FORMS');
            let numberOfForms = allOptions.length - 1;
            totalForms.setAttribute('value', `${numberOfForms}`)

        }


    }



    form.addEventListener('submit', function (e) {
        e.preventDefault()

        // if (other.classList.contains('hide')) {
        //     other.remove()
        // }

        formData = new FormData(form);
        console.log('######################')
        console.log(formData, 'formData')


        fetch(url, {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                let noError = true

                document.querySelectorAll('.error').forEach(element => {
                    element.remove()
                })
                console.log(data)

                if (data.surveyFormErrors) {
                    noError = false
                    let error = document.createElement('p');
                    error.textContent = data.surveyFormErrors.survey[0]
                    error.setAttribute('class', 'error');
                    document.querySelector('.surveyContainer .errorcontainer').appendChild(error)


                }

                if (data.questionFormErrors) {
                    noError = false

                    let error = document.createElement('p');
                    error.textContent = data.questionFormErrors.question[0];
                    error.setAttribute('class', 'error');
                    document.querySelector('.questionContainer .errorcontainer').appendChild(error)

                }

                if (noError) {
                    form.reset();
                    let otherField = document.querySelector('.otherField');
                    otherField.classList.toggle('hide');
                    let numberOfOptions = Object.keys(data.optionDict).length;

                    let preview = document.createElement('div');
                    preview.setAttribute('class', 'preview');

                    preview.setAttribute('data-id', data.questionId)

                    let survey = document.createElement('p');
                    survey.setAttribute('class', 'previewSurvey');
                    survey.textContent = data.survey;
                    preview.appendChild(survey);

                    let question = document.createElement('p');
                    question.setAttribute('class', 'previewQuestion');
                    question.textContent = data.question;
                    preview.appendChild(question);

                    let allOptionsContainer = document.createElement('div');
                    allOptionsContainer.setAttribute('class', 'previewAllOptionsContainer');

                    const object = data.optionDict
                    for (const [key, value] of Object.entries(object)) {
                        let optionContainer = document.createElement('div');
                        optionContainer.setAttribute('class', 'previewOptionContainer');
                        optionContainer.setAttribute('data-id', value);


                        let previewInput = document.createElement('input');
                        previewInput.setAttribute('class', 'previewInput');
                        previewInput.setAttribute('type', 'text');
                        previewInput.setAttribute('name', `name_${key}`);
                        previewInput.setAttribute('value', key);

                        let previewIcon = document.createElement('div');
                        previewIcon.setAttribute('class', 'previewIcon');
                        previewIcon.setAttribute('for', `name_${key}`);
                        optionContainer.appendChild(previewIcon);
                        optionContainer.appendChild(previewInput);

                        // previewIcon.innerText = key;
                        if (numberOfOptions > 1) {
                            let previewDeleteBtn = document.createElement('button');
                            previewDeleteBtn.setAttribute('class', 'previewDeleteBtn');
                            previewDeleteBtn.textContent = 'Delete';
                            previewDeleteBtn.addEventListener('click', () => {
                                deletePreviewOption(previewDeleteBtn)
                            })
                            optionContainer.appendChild(previewDeleteBtn);

                        }

                        allOptionsContainer.appendChild(optionContainer);
                    }

                    let deleteBtn = document.createElement('button');
                    deleteBtn.setAttribute('class', 'deleteBtn');
                    deleteBtn.textContent = 'Delete';
                    deleteBtn.addEventListener('click', () => {
                        deletePreview(deleteBtn.parentElement)
                    })

                    let previewAddBtn = document.createElement('button');
                    previewAddBtn.setAttribute('class', 'previewAddBtn');
                    previewAddBtn.textContent = 'Add';
                    previewAddBtn.addEventListener('click', () => {
                        addPreviewOption(previewAddBtn)
                    })

                    let error = document.createElement('p');
                    error.setAttribute('class', 'previewError');


                    preview.appendChild(allOptionsContainer);





                    if (data.showOtherForm) {
                        console.log('Shpw other form')
                        let previewOtherField = document.createElement('div')
                        previewOtherField.setAttribute('class', 'previewOtherField')
                        let previewOtherFieldInput = document.createElement('input');
                        previewOtherFieldInput.setAttribute('type', 'text')
                        previewOtherField.appendChild(previewOtherFieldInput);



                        let previewOtherFieldBtn = document.createElement('button');
                        previewOtherFieldBtn.setAttribute('type', 'button');
                        previewOtherFieldBtn.setAttribute('class', 'previewOtherFieldBtn');



                        previewOtherFieldBtn.addEventListener('click', () => {
                            deletePreviewOtherField(previewOtherFieldBtn)
                        })


                        previewOtherFieldBtn.textContent = 'Delete'
                        previewOtherField.appendChild(previewOtherFieldBtn);
                        preview.appendChild(previewOtherField);


                    } else {
                        console.log('dont show other form')
                    }

                    preview.appendChild(deleteBtn)
                    preview.appendChild(previewAddBtn)
                    preview.appendChild(error)
                    // i am here 










                    document.querySelector('.previewContainer').appendChild(preview)
                    resetOptions();

                }


            })
            .catch((error) => {
                console.error('Error:', error);


            });


    })

    function addPreviewOption(element) {


        let originalList = element.parentElement.querySelectorAll('.previewOptionContainer');

        let original = originalList[originalList.length - 1];
        if (originalList.length == 1) {
            let removeBtn = document.createElement('button');
            removeBtn.textContent = 'Delete';

            removeBtn.setAttribute('class', 'previewDeleteBtn');
            removeBtn.setAttribute('type', 'button');
            removeBtn.addEventListener('click', () => {
                // removeOption(removeBtn)
                alert('j09ioköl')

            })
            original.appendChild(removeBtn)
        }

        let dataId = parseInt(original.getAttribute('data-id')) + 1;

        let allOptions = original.parentElement

        let copy = original.cloneNode(true);
        // copy.setAttribute('data-id', dataId)
        copy.setAttribute('data-id', '')
        copy.querySelector('input').value = '';
        copy.querySelector('input').addEventListener('focusout', () => {
            submitPreviewOption(copy.querySelector('input'))
        })
        let copyBtn = copy.querySelector('.previewDeleteBtn');
        copyBtn.addEventListener('click', () => {
            // removeOption(copyBtn)
            // alert('j09ioköl')
            // deletePreview(copy)
            deletePreviewOption(copyBtn)
        })



        allOptions.appendChild(copy)


    }

    function submitPreviewOption(element) {
        let questionId = element.parentElement.parentElement.parentElement.getAttribute('data-id')

        let question = element.parentElement
        let dataId = element.parentElement.getAttribute('data-id')


        let formData = new FormData();
        formData.append('addPreviewOption', element.value);
        formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
        formData.append('questionId', questionId);



        if (dataId) {
            formData.append('dataId', dataId);
        }

        fetch(url, {
            method: 'POST',
            body: formData,
        })

            .then(response => response.json())
            .then(data => {

                question.setAttribute('data-id', data.dataId)

            })
            .catch((error) => {
                console.log('error', error)
            })
    }

    function removePreviewOption(element) {
        let option = element.parentElement;
        option.remove()
    }

    function addOption() {

        let allOptions = document.querySelectorAll('.optionContainer');

        let totalForms = document.querySelector('#id_form-TOTAL_FORMS');
        let numberOfForms = allOptions.length - 1;
        let newOption = allOptions[0].cloneNode(true);
        let formRegex = RegExp(`form-(\\d){1}-`, 'g');
        numberOfForms++;


        let label = newOption.querySelector('label');


        label.setAttribute('for', `id_form-${numberOfForms}-option`)

        let input = newOption.querySelector('input');
        input.value = '';
        input.setAttribute('id', `id_form-${numberOfForms}-option`)
        input.setAttribute('name', `form-${numberOfForms}-option`)

        let hiddenInput = newOption.querySelector('.option').querySelectorAll('input')[1];

        hiddenInput.setAttribute('id', `id_form-${numberOfForms}-id`)
        hiddenInput.setAttribute('name', `form-${numberOfForms}-id`)



        let allOptionsContainer = document.querySelector('.allOptionsContainer');

        allOptionsContainer.appendChild(newOption)
        totalForms.setAttribute('value', `${numberOfForms + 1}`)
        updateBtnList(newOption.querySelector('.removeBtn'))
    }

    function resetOptions() {

        let allOptions = Array.from(document.querySelectorAll('.optionContainer'));
        if (allOptions.length > 0) {

            for (index = 1; index < allOptions.length; index++) {
                allOptions[index].remove()

            }
            document.querySelector('#id_form-TOTAL_FORMS').value = 1;
        }


    }

    function deletePreview(element) {
        let data = new FormData()

        data.append('csrfmiddlewaretoken', '{{ csrf_token }}');
        let id = element.getAttribute('data-id')

        data.append('deleteQuestion', id)



        fetch(url, {
            method: 'POST',
            body: data,
        })
            .then(response => response.json())
            .then(data => {

                element.remove()
            })

            .catch((error) => {
                console.log('Error', error)
            })
    }