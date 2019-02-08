"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session,url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    # if session['user_id']:
    #     print(session['user_id'])
    #     user_session = session.user_id
    # else:
    #     user_session = None
    
    return render_template("homepage.html")

@app.route('/movies')
def show_movie():

    movies = Movie.query.order_by(Movie.title).all()


    return render_template('all_movies.html', movies=movies)

@app.route('/movies-info/<movie_id>')
def show_movie_info(movie_id):


    movie = Movie.query.get(movie_id)

    ratings = Rating.query.filter_by(movie_id=movie_id).all()


    return render_template('movie_details.html', movie=movie, ratings=ratings)


@app.route('/add-rating')
def add_rating():

    score = request.args.get('score')
    new_score = Rating(score=score)

    db.session.add(new_score)
    db.session.commit()
    flash("You have added a new rating!")

    # movie_id = db.session.query(Movie).filter_by(title=title).first()
    return redirect('movies-info')

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)

@app.route('/user-info/<user_id>')
def show_user_info(user_id):

    print('USER ID:', user_id)
    # users = User.query.all()
    user = User.query.get(user_id)
    print('user:', user)
    # movies = db.session.query(Rating).filter_by(user_id=user_id)


    # users_id = db.session.query(User.user_id).filter_by(email=email).first()


    # user_id = request.args.get('user_id')



    return render_template("user_details.html", user=user)

@app.route('/register', methods=["GET"])
def register_form():

    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def register_process():

    email = request.form.get("email")
    password = request.form.get("password")

    # finding id to log user in because we do not have
    #emails
    user = db.session.query(User.user_id).filter_by(email=email).first()
    print('USER:', user)

    if user == None:

        new_user = User(email=email, password=password)

        db.session.add(new_user)
        db.session.commit()
        flash('You\'ve been added!')
        return redirect("/") 
    else:
        session['user_id'] = user[0]
        print('\n\n\n\n\n')
        print('HI')    
        flash('You are logged in!')
        return redirect('user-info/' + str(user[0]))
        # return redirect(url_for('show_user_info', user_id=user[0]))

@app.route('/logout')
def logout():

    del session['user_id']

    return redirect('/')
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
