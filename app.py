# external libraries
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_session import Session

from flask_wtf import FlaskForm
from wtforms import DateField, validators, SubmitField
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import getenv
import jsonpickle


class DateInput(FlaskForm):
    date = DateField("Day to Learn About", validators=(validators.DataRequired(),))
    submit = SubmitField("Submit")


# internal libraries
from date_information import DateInformation

load_dotenv()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = getenv("FLASK_APP_SECRET_KEY")
Session(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/date_input/", methods=["POST", "GET"])
def date_input():
    form = DateInput()
    if form.validate_on_submit():
        date_information = DateInformation(form.date.data)
        session["date_information"] = date_information.toJSON()
        return redirect(url_for("view"))
    if request.method == "POST":
        pass
    else:
        return render_template("date_input.html", form=form)


@app.route("/todo/")
def todo():
    return render_template("todo.html")


@app.route("/view/", methods=["GET", "POST"])
def view():
    date_information = jsonpickle.decode(session["date_information"])
    return render_template("view.html", date=date_information.date)


if __name__ == "__main__":
    app.run(debug=True)
