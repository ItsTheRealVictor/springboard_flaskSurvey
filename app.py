from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, personality_quiz, satisfaction_survey, surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "farts"
app.debug = True
debug = DebugToolbarExtension(app)

RESPONSES = []



@app.route('/')
def main_page():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)