from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Course, Base

# Before running this, actually create a temporary postgres database::
#
#     createdb tinker
#


def show(sess, description):
    """Display the entire contents of a database session with these tables"""
    print("=" * 10, "begin", description, "=" * 10)

    for cls in (Student, Course):
        for obj in sess.query(cls).all():
            print(obj)

    print()

    for s in sess.query(Student).all():
        print(f"{s.name}:", ", ".join(c.title for c in s.courses))

    print("=" * (28 + len(description)))
    print()


# Fill in your own name, host, dbname here, if you want to mess around...
engine = create_engine("postgresql+psycopg2://fiddle@localhost/tinker")

### Create any tables not already present.
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
work_session = Session()

### Ensure an empty database (so you can run this script more than once)
for cls in (Student, Course):
    for obj in work_session.query(cls).all():
        work_session.delete(obj)

### Build non-empty initial state
fred = Student(id=1, name="Fred Brooks")
diana = Student(id=4, name="Diana Shirley")

phy = Course(id=2, title="Phy 101")
cs = Course(id=3, title="CS Basics")

fred.courses = [cs]
diana.courses = [phy]

for it in (fred, diana, phy, cs):
    work_session.merge(it)

work_session.commit()
show(work_session, "init state")

### Open up a second session on the same engine
read_session = Session()

### Make some changes in the work_session
elaine = Student(id=5, name="Elanor Rigby")
math = Course(id=4, title="Calc 7", students=[fred, diana, elaine])

work_session.merge(elaine)
work_session.merge(math)
fred.name = "Frederic Brooks"

### We haven't committed yet. Look at the session states.
show(work_session, "work session")
show(read_session, "old read session")

### Double check that changes to "Fred Brooks" show up only in objects
### related to things in the work_session, and not in objects related
### to the read_session.
print("Math students")
for s in math.students:
    print(s)
old_cs = read_session.query(Course).filter(Course.id == 3).one()

print("(Old) CS students")
for s in old_cs.students:
    print(s)

print()
### Finally, commit the work_session
work_session.commit()

### And see that both sessions look the same now
show(work_session, "work session after commit")
show(read_session, "read session after commit")
