from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterUserForm, LoginForm


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def redirect_to_register():
    """ redirect to the register page """
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user: produce form & handle form submission."""
    form = RegisterUserForm()
    if form.validate_on_submit():
        form_data = {key: value for (key, value) in form.data.items()
                     if key != "csrf_token"}
        user = User.register(**form_data)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return redirect("/secret")
    else:
        return render_template("/register", form=form)
