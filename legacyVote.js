var legit = 'yes'
    let voteForm = document.querySelector('#voteForm');
    let loadBtn = document.querySelector('.load');
    let optionSelect = voteForm.querySelector('#id_voteForm-option');
    let questionSelect = voteForm.querySelector('#id_voteForm-question');
    let questions = Array.from(document.querySelectorAll('.questionContainer'));
    let surveyId = document.querySelector('h1').getAttribute('data-id')

    let url = "{% url 'takeSurvey' 0 %}".replace('0', surveyId)

    document.querySelector('#legit').addEventListener('click', () => {
        console.log('legit: ', legit)
    })

    loadBtn.addEventListener('click', loadForm);
    var allGood = 1
    function loadForm() {
        
        console.log(questions.length)
        questions.forEach(question => {

            console.log('index: ', questions.indexOf(question))
            // let questionName = question.querySelector('.question').textContent;
            let questionName = question.querySelector('.question');
            let options = Array.from(question.querySelectorAll('.option'));

            options.forEach(option => {
                let vote = option.querySelector('input');
                if (vote.checked) {

                   

                    if (questions.indexOf(question) == questions.length - 1) {
                        console.log('last quesrion')
                        submitVote(vote.value, questionName, 'last')
                    } else {
                        submitVote(vote.value, questionName, 'not last')
                    }



                }
            })

        })


    }

    function submitVote(vote, question, position) {

        let options = Array.from(optionSelect.options)
        let questionOptions = Array.from(questionSelect.options)

        questionOptions.forEach(questionOption => {
            if (questionOption.textContent == question.textContent) {
                // questionOption.selected = 'selected';
                // questionOption.setAttribute("selected", '')
            } else {
                questionOption.selected = false;
                questionOption.removeAttribute("selected")
            }
        });

        options.forEach(option => {

            if (option.textContent == vote) {

                // option.selected = 'selected';
                // option.setAttribute("selected", '')
                let formdata = new FormData(voteForm)
                formdata.append('position', position);
                formdata.append('allGood', allGood);
                fetch(url, {
                    method: 'POST',
                    body: formdata,
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data)
                        let errorP = question.parentElement.querySelector('.error')
                        errorP.textContent = '';

                        if (data.error) {
                            legit = 'no'
                            allGood -= 1

                            for (const [key, value] of Object.entries(data.error)) {
                                // console.log(`${key}: ${value}`);
                                errorP.textContent += value + ' ';
                            }
                        } else {

                        }
                    })
                    .catch(error => { console.log(error) })

            } else {
                option.selected = false;
                option.removeAttribute("selected")
            }
        });
    }
