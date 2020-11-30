# A few trivial models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

student_course = Table(
    "student_course",
    Base.metadata,
    Column("student", Integer, ForeignKey("students.id")),
    Column("course", Integer, ForeignKey("courses.id")),
)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    courses = relationship(
        "Course",
        secondary=student_course,
        back_populates="students",
        cascade="all, delete",
    )

    def __repr__(self):
        return f"Student({self.id}, {self.name})"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    students = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses",
        cascade="all, delete",
    )

    def __repr__(self):
        return f"Course({self.id}, {self.title})"
