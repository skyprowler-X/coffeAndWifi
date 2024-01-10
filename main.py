from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL
import csv
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
Bootstrap(app)


def add_data(new_data: list):
    with open("cafe-data.csv", "a", newline="", encoding="UTF-8") as csv_file:
        csv_data = csv.writer(csv_file, delimiter=",")
        csv_data.writerow(new_data)


class CafeForm(FlaskForm):
    cafe = StringField("Cafe name", validators=[DataRequired()])
    localization_url = StringField(
        "Cafe localization on google maps",
        validators=[DataRequired(), URL()],
    )
    opening = StringField("Opening time e.g. 8AM", validators=[DataRequired()])
    closing = StringField("Closing time e.g 5:30PM", validators=[DataRequired()])
    caffe_rating = SelectField(
        "cofee rating",
        validators=[DataRequired()],
        choices=["\u2615" * i for i in range(6) if i > 0],
    )
    wifi_rating = SelectField(
        "Wifi strength rating",
        validators=[DataRequired()],
        choices=["\U0001F4AA" * i if i > 0 else "\U00002718" for i in range(6)],
    )
    power_sockets = SelectField(
        "Power socket availibles",
        validators=[DataRequired()],
        choices=["\U0001F50C" * i if i > 0 else "\U00002718" for i in range(6)],
    )
    submit = SubmitField("Submit")


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_data = []
            for field in form.data.items():
                if "submit" == field[0]:
                    break
                else:
                    new_data.append(field[1])
            add_data(new_data)
    return render_template("add.html", form=form)


@app.route("/cafes")
def cafes():
    print(os.getcwd())
    with open("cafe-data.csv", newline="", encoding="UTF-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)

    return render_template("cafes.html", cafes=list_of_rows)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
