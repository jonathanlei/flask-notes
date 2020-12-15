from app import app
from models import User, Note, db

db.drop_all()
db.create_all()


user = User.register(username="testUser",
                     password="testPassword",
                     email="testuser@testuser.com",
                     first_name="testFirst",
                     last_name="testLast")
db.session.add(user)
db.session.commit()
user.notes.append(Note(title="testTitle", content="testContent"))
db.session.commit()
