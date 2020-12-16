from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Note
from forms import RegisterUserForm, LoginForm, AddNoteForm, EditNoteForm, DeleteUserForm, DeleteNoteForm

from werkzeug.exceptions import Unauthorized


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

REGISTER_WHITELIST = {"username", "password", "first_name", "last_name", "email"}
LOGIN_WHITELIST = {"username", "password"}
USER_ID = "user_id"


@app.route("/")
def redirect_to_register():
    """ redirect to the register page """
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user: produce form & handle form submission."""
    form = RegisterUserForm()
    if form.validate_on_submit():
        form_data = {
            key: value
            for (key, value) in form.data.items()
            if key in REGISTER_WHITELIST
        }

        user = User.register(**form_data)
        db.session.add(user)
        db.session.commit()

        session[USER_ID] = user.username

        return redirect(f"/users/{user.username}")
    else:
        return render_template("register_user.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Login user: produce form and handle form submission """

    form = LoginForm()

    if form.validate_on_submit():
        form_data = {
            key: value for (key, value) in form.data.items() if key in LOGIN_WHITELIST
        }

        user = User.authenticate(**form_data)

        if user:
            session["user_id"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Bad username / password"]

    return render_template("login_user.html", form=form)

@app.route("/logout")
def logout():
    """ Logout user and redirect to homepage"""

    session.pop("user_id", None)

    return redirect("/")


@app.route("/users/<username>")
def get_user(username):
    """ Shows information about the user at username if logged in """

    if session.get("user_id") != username:
        raise Unauthorized(description="You do not have permission!")
    else:
        user = User.query.get(username)
        return render_template("show_user.html", user=user, 
                                                delete_note_form=DeleteNoteForm(), 
                                                delete_user_form=DeleteUserForm())


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """ find user and delete from the database,
    clear session data and redirect to / """

    if session.get("user_id") != username:
        raise Unauthorized(description="You do not have permission!")

    form = DeleteUserForm()
    user = User.query.get_or_404(username)

    if form.validate_on_submit():

        db.session.query(Note).filter(Note.owner == user.username).delete()
        db.session.delete(user)
        db.session.commit()

        session.pop("user_id", None)

        return redirect("/")


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_note(username):
    """ add note for user given username: produce form & handle form submission."""

    if session.get("user_id") != username:
        raise Unauthorized(description="You do not have permission!")

    form = AddNoteForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner=username)
        db.session.add(note)
        db.session.commit()

        return redirect(f"/users/{username}")
    else:
        return render_template("add_note.html", form=form)
    

@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """ update note for the given note id: produce form & handle form submission."""

    note = Note.query.get_or_404(note_id)
    if session.get("user_id") != note.owner:
        raise Unauthorized(description="You do not have permission!")
    
    form = EditNoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{note.owner}")
    else:
        return render_template("edit_note.html", form=form, note=note)

@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    """ delete a note if the user is verified, and redirect to users page """

    # Make sure to do a form validation with DeleteForm to protect from CSRF attack
    # Also check out raise Unauthorized
    note = Note.query.get_or_404(note_id)
    if session.get("user_id") != note.owner:
        raise Unauthorized(description="You do not have permission!")
    
    form = DeleteNoteForm()
    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()
        return redirect(f"/users/{note.owner}")
    
    

# Further Study: Maybe refactor the validation function for logged in user
# def validate_session()