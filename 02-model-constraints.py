from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
db = SQLAlchemy(app)


class User(db.Model):
	__tablename__ = "user"

	id = db.Column(db.Integer, primary_key=True)
	passport_number = db.Column(db.String(3), unique=True)
	name = db.Column(db.String(100), nullable=False)
	age = db.Column(db.Integer, db.CheckConstraint("age > 18"))
	group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

	group = relationship("Group")
	# group = relationship("Group", back_populates="users")


class Group(db.Model):
	__tablename__ = "group"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))

	# users = relationship("User")
	users = relationship("User", back_populates="group")


app.app_context().push()
db.create_all()

# PK Unique Exception
try:
	user_01 = User(id=1, name="User #1", age=30, passport_number="123")

	with db.session.begin():
		db.session.add(user_01)

	user_01_copy = User(id=2, name="User #1", age=30, passport_number="456")

	with db.session.begin():
		db.session.add(user_01_copy)
except Exception as e:
	print(e)


# Column Unique Exception
try:
	user_02 = User(id=3, name="User #2", age=35, passport_number="234")

	with db.session.begin():
		db.session.add(user_02)
except Exception as e:
	print(e)

# Check Exception
try:
	user_03 = User(id=4, name="User #4", age=19, passport_number="345")

	with db.session.begin():
		db.session.add(user_03)
except Exception as e:
	print(e)


# Nullable Exception
try:
	user_04 = User(id=5, name="None", age=19, passport_number="777")

	with db.session.begin():
		db.session.add(user_04)
except Exception as e:
	print(e)
