import crud
from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import StudentSchema, ClassSchema, InstructorSchema, StudentInterestSchema, Request, Response, RequestStudent, RequestClass, RequestInstructor, RequestStudentInterest, student_model_to_schema, class_model_to_schema, instructor_model_to_schema, student_interest_model_to_schema
from typing import Annotated
from models import User

import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request
import json
from fastapi.encoders import jsonable_encoder

router = APIRouter()
authentication = APIRouter()
json_filename="user.json"

with open(json_filename, "r") as read_file:
    data = json.load(read_file)

def write_data(data):
    with open(json_filename, "w") as write_file:
        json.dump(data, write_file, indent=4)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
JWT_SECRET = 'myjwtsecret'
ALGORITHM = 'HS256'

def get_user_by_username(username):
    for desain_user in data['user']:
        if desain_user['username'] == username:
            return desain_user
    return None

def authenticate_user(username: str, password: str):
    user_data = get_user_by_username(username)
    if not user_data:
        return None

    user = User(id=user_data['id'], username=user_data['username'], password_hash=user_data['password_hash'])

    if not user.verify_password(password):
        return None

    return user

@authentication.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        print(f"Invalid username or password for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )

    token = jwt.encode({'id': user.id, 'username': user.username}, JWT_SECRET, algorithm=ALGORITHM)

    return {'access_token': token, 'token_type': 'bearer'}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = get_user_by_username(payload.get('username'))
        return User(id=user['id'], username=user['username'], password_hash=user['password_hash'])
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

@authentication.post('/users')
async def create_user(username: str, password: str):
    last_user_id = data['user'][-1]['id'] if data['user'] else 0
    user_id = last_user_id + 1
    user = jsonable_encoder(User(id=user_id, username=username, password_hash=bcrypt.hash(password)))
    data['user'].append(user)
    write_data(data)
    return {'message': 'User created successfully'}

@authentication.get('/users/me')
async def get_user(user: User = Depends(get_current_user)):
    return {'id': user.id, 'username': user.username, 'role': 'admin'}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/students/create")
async def create_student_service(request: RequestStudent, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        student = crud.create_student(db, student=request.parameter)
        student_schema = student_model_to_schema(student)
        return Response(status="Ok", code="200", message="Student created successfully", result=student_schema)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/students/")
async def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    students = crud.get_students(db, skip, limit)
    student_schemas = [student_model_to_schema(student) for student in students]
    return Response(status="Ok", code="200", message="Success fetch all students", result=student_schemas)

@router.post("/classes/create")
async def create_class_service(request: RequestClass, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        class_ = crud.create_class(db, class_=request.parameter)
        class_schema = class_model_to_schema(class_)
        return Response(status="Ok", code="200", message="Class created successfully", result=class_schema)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/classes/")
async def get_classes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    classes = crud.get_classes(db, skip, limit)
    class_schemas = [class_model_to_schema(class_) for class_ in classes]
    return Response(status="Ok", code="200", message="Success fetch all classes", result=class_schemas)

@router.post("/instructors/create")
async def create_instructor_service(request: RequestInstructor, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        instructor = crud.create_instructor(db, instructor=request.parameter)
        instructor_schema = instructor_model_to_schema(instructor)
        return Response(status="Ok", code="200", message="Instructor created successfully", result=instructor_schema)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/instructors/")
async def get_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    instructors = crud.get_instructors(db, skip, limit)
    instructor_schemas = [instructor_model_to_schema(instructor) for instructor in instructors]
    return Response(status="Ok", code="200", message="Success fetch all instructors", result=instructor_schemas)

@router.post("/studentinterests/add")
async def add_student_interest_service(request: RequestStudentInterest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        student_id = request.parameter.student_id
        interest = request.parameter.interest
        crud.add_student_interest(db, student_id, interest)
        return Response(status="Ok", code="200", message="Interest added successfully", result=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/studentinterests/remove")
async def remove_student_interest_service(request: RequestStudentInterest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        student_id = request.parameter.student_id
        interest = request.parameter.interest
        crud.remove_student_interest(db, student_id, interest)
        return Response(status="Ok", code="200", message="Interest removed successfully", result=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/students/recommendations/{student_id}")
async def get_student_recommendations(student_id: int = Path(..., title="Student ID", description="The student's ID"), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    recommendations = crud.get_class_recommendations(db, student_id)
    class_schemas = [class_model_to_schema(class_) for class_ in recommendations]
    return Response(status="Ok", code="200", message="Recommendations based on student's interest", result=class_schemas)

@router.get("/instructors/recommendations/{student_id}")
async def get_instructor_recommendations(student_id: int = Path(..., title="Student ID", description="The student's ID"), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    recommendations = crud.get_instructor_recommendations(db, student_id)
    instructor_schemas = [instructor_model_to_schema(instructor) for instructor in recommendations]
    return Response(status="Ok", code="200", message="Recommendations based on student's interest", result=instructor_schemas)