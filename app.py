# external libraries
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import date
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
from os import getenv

# internal libraries
from date_information import DateInformation


def flash_future_dates(form, field):
    if field.data > date.today():
        flash(
            "We can't possibly know the future, you silly goose...but we've got data from other years!"
        )
        return


class DateInput(FlaskForm):
    date = DateField(
        "Day to Learn About",
        validators=(
            DataRequired(),
            flash_future_dates,
        ),
    )
    submit = SubmitField("Submit")


load_dotenv()

app = Flask(__name__)
app.secret_key = getenv("FLASK_APP_SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/date_input/", methods=["POST", "GET"])
def date_input():
    form = DateInput()
    if form.validate_on_submit():
        date_for_session = [
            form.date.data.month,
            form.date.data.day,
            form.date.data.year,
        ]
        # date_information = DateInformation(form.date.data)
        session["date_for_session"] = date_for_session
        return redirect(url_for("output"))
    if request.method == "GET":
        return render_template("date_input.html", form=form)


@app.route("/output/", methods=["GET", "POST"])
def output():
    if session.get("date_for_session"):
        date_from_session = date(
            month=session["date_for_session"][0],
            day=session["date_for_session"][1],
            year=session["date_for_session"][2],
        )
        date_information = DateInformation(date_from_session)
        session.pop("date_for_session")
        return render_template(
            "output.html",
            date_information=date_information,
            today=date.today(),
            formatted_full_date=date_information.date.strftime("%A, %B %d, %Y"),
            formatted_month_day=date_information.date.strftime("%B %d"),
        )
    else:
        return redirect(url_for("date_input"))


if __name__ == "__main__":
    app.run(debug=True)
