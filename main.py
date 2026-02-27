from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

THEMOVIEDB_BASE_URL = "https://api.themoviedb.org/3/search/movie"
ACCESS_TOKEN = ""
API_KEY = ""

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# CREATE DB

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///top_movies.db'

db.init_app(app)

# CREATE TABLE

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column(Float, default = 0)
    ranking: Mapped[int] = mapped_column(Integer, default=0)
    review: Mapped[str] = mapped_column(String, nullable=True)
    img_url: Mapped[str] = mapped_column(String, nullable=False)

with app.app_context():
    db.create_all()

# Add the first entry into database

# with app.app_context():
#     new_movie = Movie(
#         title="Phone Booth",
#         year=2002,
#         description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's "
#                     "sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to"
#                     " a jaw-dropping climax.",
#         rating=7.3,
#         ranking=10,
#         review="My favourite character was the caller.",
#         img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#     )
#
#     db.session.add(new_movie)
#     db.session.commit()

# Create Movie Edit Flask Form

class MoviesEditForm(FlaskForm):
    rating = FloatField("Rating", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create Movie Add Flask Form

class MovieAddForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/")
def home():

    result = db.session.execute(db.select(Movie))
    movies = result.scalars()
    return render_template("index.html", movies=movies)

@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):

    # Get the movie we want to update

    movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == int(movie_id))).scalar()

    # Create a form instance

    form = MoviesEditForm()

    # Update the table entry if the submit button was pressed

    if form.validate_on_submit():
        movie_to_update.rating = form.rating.data
        movie_to_update.review = form.review.data
        db.session.commit()

        return redirect(url_for("home"))

    # The final thing is to render the edit.html page



    return render_template("edit.html", form=form, movie_id=movie_id)

@app.route("/delete/<int:movie_id>", methods=["GET", "POST"])
def delete(movie_id):

    movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == int(movie_id))).scalar()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/add", methods=["GET", "POST"])
def add():
    form = MovieAddForm()

    print("Method:", request.method)

    if form.validate_on_submit():
        # print("Form validated")
        movie_title = form.title.data
        # print("Movie title:", movie_title)
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "accept": "application/json"
        }

        response = requests.get(
            url=THEMOVIEDB_BASE_URL,
            params={
                "query": movie_title,
                "include_adult": "false",
                "language": "en-US",
                "page": 1
            },
            headers=headers
        )

        # print("Status:", response.status_code)
        # print("Response:", response.text)

        results = response.json()["results"]

        # print("Results:", results)

        return render_template("select.html", movies = results)

    # print("Form errors:", form.errors)

    return render_template("add.html", form=form)

@app.route("/select/<int:movie_id>")
def select(movie_id):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "accept": "application/json"
    }
    params = {
        "language": "en-US"
    }
    response = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}", params = params, headers=headers)

    data = response.json()

    selected_movie = Movie(
        title=data["original_title"],
        year=data["release_date"].split("-")[0],
        description=data["overview"],
        img_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}",
    )
    db.session.add(selected_movie)
    db.session.commit()

    #return redirect(url_for("home"))

    movie_to_update = db.session.execute(db.select(Movie).where(Movie.title == data["original_title"])).scalar()

    return redirect(url_for("edit", movie_id=movie_to_update.id))

if __name__ == '__main__':
    app.run(debug=True)
