from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, desc, func
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

# Подготовка данных
group_01 = Group(id=1, name="Group #1")
group_02 = Group(name="Group #2")

user_01 = User(id=1, name="John", age=20, group=group_01)
user_02 = User(name="Kate", age=22, group=group_02)
user_03 = User(name="Artur", age=23, group=group_01)
user_04 = User(name="Maxim", age=24, group=group_01)
user_05 = User(name="Lily", age=25, group=group_02)
user_06 = User(name="Marie", age=26, group=group_02)

with db.session.begin():
	db.session.add_all([
		user_01,
		user_02,
		user_03,
		user_04,
		user_05,
		user_06,
	])


# Запросы данных

"""
SQL -> WHERE
query = User.query.filter(User.name == 'John')
"""
query = db.session.query(User).filter(User.name == 'John')
# print(f"Запрос: {query}")
# print(f"Результат: {query.first().name}")


"""
SQL -> WHERE (Required RECORD)
query = User.query.filter(User.name == 'John')
"""
try:
	query = db.session.query(User).filter(User.name == 'John')
	# print(f"Запрос: {query}")
	# print(f"Результат: {query.one()}")
except Exception as e:
	print("Ошибка: ", e)


"""
SQL -> WHERE ... AND
"""
query = db.session.query(User).filter(User.id <= 5, User.age > 20)
# print(f"Запрос: {query}")
# print(f"Результат: {query.all()}")


"""
SQL -> LIKE
"""
query = db.session.query(User).filter(User.name.like('M%'))
# print(f"Запрос: {query}")
# print(f"Результат: {query.all()}")


"""
SQL -> WHERE ... OR ...
"""
query = db.session.query(User).filter(
	or_(User.id <= 5, User.age > 20)
)
# print(f"Запрос: {query}")
# print(f"Результат: {query.all()}")


"""
SQL -> WHERE ... IS NULL
"""
query = db.session.query(User).filter(User.passport_number == None)
# print(f"Запрос: {query}")
# print(f"Результат: {query.all()}")


"""
SQL -> WHERE ... IS NOT NULL
"""
query = db.session.query(User).filter(User.passport_number != None)
# print(f"Запрос: {query}")
# print(f"Результат: {query.all()}")


"""
SQL -> WHERE ... IN (...)
"""
query = db.session.query(User).filter(User.id.in_([1, 3]))
# print(f"Запрос: {query}")
# print(f"Результат: {query.all()}")


"""
SQL -> WHERE ... NOT IN (...)
"""
query = db.session.query(User).filter(User.id.notin_([1, 3]))
# print(f"Запрос: {query}")
# print(f"Результат: {query.all()}")


"""
SQL -> WHERE ... BETWEEN ... AND ...
"""
query = db.session.query(User).filter(User.id.between(1, 6))
# print(f"Запрос: {query}")
# print(f"Результат: {query.all()}")


"""
SQL -> LIMIT ...
"""
query = db.session.query(User).limit(2)
# print(f"Запрос: {query}")
# print(f"Результат: {query.all()}")


"""
SQL -> LIMIT ... OFFSET ...
"""
query = db.session.query(User).limit(2).offset(2)
# print(f"Запрос: {query}")
# print(f"Результат: {query.all()}")


"""
SQL -> ORDER BY ... (сортировка)
"""
query = db.session.query(User).order_by(User.id)
# print(f"Запрос: {query}")
# print(f"Результат: {query.all()}")
query = db.session.query(User).order_by(desc(User.id))
# print(f"Запрос: {query}")
# print(f"Результат: {query.all()}")


"""
SQL -> JOIN ... (inner join)
"""
query = db.session.query(User.name, Group.name).join(Group)
# print(f"Запрос: {query}")
# print(f"Результат: {query.all()}")


"""
SQL -> JOIN ... (outer left join)
"""
query = db.session.query(User.name, Group.name).join(Group, isouter=True)
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")


"""
SQL -> GROUP BY ... (scalar)
func -> count(User.id)
"""
query = db.session.query(func.count(User.id)).join(Group).filter(Group.id == 1).group_by(Group.id)
# print(f"Запрос: {query}")
# print(f"Результат: {query.scalar()}")
