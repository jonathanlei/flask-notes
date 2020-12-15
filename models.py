"""Models for notes app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ Make a user """

    __tablename__ = "users"
    
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text(), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """ Register user w/hashed password & return user."""
        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(
                   username=username,
                   password=hashed,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, password):
        """ Validate that user exists and password provided is correct 
        
        Returns user if valid, else return False
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Note(db.Model):
    """ Make a note """

    __tablename__ = "notes"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    owner = db.Column(db.String(20),
                      db.ForeignKey("users.username"),
                      nullable=False)
    user = db.relationship("User", backref="notes")
