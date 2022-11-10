from flask import Flask, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey, surveys



RESPONSES_KEY = "responses"
app = Flask(__name__)

app.config['SECRET_KEY'] = "farts"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
debug = DebugToolbarExtension(app)


survey_questions = {id : quest.question for id, quest in enumerate(satisfaction_survey.questions)}
quest_ids = [x for x in range(1, len(survey_questions.keys()) + 1)]


@app.route("/")
def show_survey_start():
    """Select a survey."""

    return render_template("survey_start.html", satisfaction_survey=satisfaction_survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def question_handler():
    
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/questions/<int:quest_num>')
def show_first_question(quest_num):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != quest_num):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {quest_num}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[quest_num]
    return render_template(
        "questions.html", question_num=quest_num, question=question)


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")

if __name__ == '__main__':
    app.run(debug=True)