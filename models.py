from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config import Base, SessionLocal

class Users (Base) : 
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)

class Student(Base):
    __tablename__ = "student"  # Mengganti "user" menjadi "student"

    student_id = Column(Integer, primary_key=True, index=True)  # Mengganti "user_id" menjadi "student_id"
    username = Column(String)
    fullname = Column(String)
    email = Column(String)
    interest = Column(String)

    # Menyambungkan Student dengan minat mereka
    interests = relationship("StudentInterest", back_populates="student")  # Mengganti "UserInterest" menjadi "StudentInterest"

class Class(Base):
    __tablename__ = "class"

    class_id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String)
    class_description = Column(String)
    class_instructor = Column(Integer, ForeignKey('instructor.instructor_id'))

    # Menyambungkan Class dengan Instructor
    instructor = relationship("Instructor", back_populates="classes")

class Instructor(Base):
    __tablename__ = "instructor"

    instructor_id = Column(Integer, primary_key=True, index=True)
    instructor_name = Column(String)
    instructor_bio = Column(String)
    instructor_specialty = Column(String)

    # Menyambungkan Instructor dengan kelas yang dia ajar
    classes = relationship("Class", back_populates="instructor")

class StudentInterest(Base):
    __tablename__ = "student_interest"  # Mengganti "user_interest" menjadi "student_interest"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('student.student_id'))  # Mengganti "user_id" menjadi "student_id"
    interest = Column(String)

    # Menyambungkan StudentInterest dengan Student
    student = relationship("Student", back_populates="interests")  # Mengganti "User" menjadi "Student"

# Fungsi untuk mengambil rekomendasi
def get_recommendations(student_id):
    session = SessionLocal()
    try:
        # Mendapatkan minat pengguna
        student_interests = session.query(StudentInterest.interest).filter(StudentInterest.student_id == student_id).all()  # Mengganti "UserInterest" menjadi "StudentInterest"
        student_interests = [interest[0] for interest in student_interests]

        # Mencari kelas yang sesuai dengan minat pengguna
        recommended_classes = session.query(Class).join(Instructor, Instructor.instructor_id == Class.class_instructor).filter(Class.class_instructor != student_id, Instructor.instructor_specialty.in_(student_interests)).all()

        return recommended_classes
    finally:
        session.close()