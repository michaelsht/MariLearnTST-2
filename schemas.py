from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
import models
from uuid import UUID

T = TypeVar('T')

class StudentSchema(BaseModel):
    student_id: Optional[int] = None  # Mengganti "user_id" menjadi "student_id"
    username: Optional[str] = None
    fullname: Optional[str] = None
    email: Optional[str] = None
    interest: Optional[str] = None

    class Config:
        orm_mode = True

class ClassSchema(BaseModel):
    class_id: Optional[int] = None
    class_name: Optional[str] = None
    class_description: Optional[str] = None
    class_instructor: Optional[int] = None

    class Config:
        orm_mode = True

class InstructorSchema(BaseModel):
    instructor_id: Optional[int] = None
    instructor_name: Optional[str] = None
    instructor_bio: Optional[str] = None
    instructor_specialty: Optional[str] = None

    class Config:
        orm_mode = True

class StudentInterestSchema(BaseModel):
    id: Optional[int] = None
    student_id: Optional[int] = None  # Mengganti "user_id" menjadi "student_id"
    interest: Optional[str] = None

    class Config:
        orm_mode = True

class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)

class RequestStudent(BaseModel):
    parameter: StudentSchema = Field(...)

class RequestClass(BaseModel):
    parameter: ClassSchema = Field(...)

class RequestInstructor(BaseModel):
    parameter: InstructorSchema = Field(...)

class RequestStudentInterest(BaseModel):
    parameter: StudentInterestSchema = Field(...)

class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]

def student_model_to_schema(student: models.Student) -> StudentSchema:
    return StudentSchema(
        student_id=student.student_id,  # Mengganti "user_id" menjadi "student_id"
        username=student.username,
        fullname=student.fullname,
        email=student.email,
        interest=student.interest
    )

def class_model_to_schema(class_: models.Class) -> ClassSchema:
    return ClassSchema(
        class_id=class_.class_id,
        class_name=class_.class_name,
        class_description=class_.class_description,
        class_instructor=class_.class_instructor
    )

def instructor_model_to_schema(instructor: models.Instructor) -> InstructorSchema:
    return InstructorSchema(
        instructor_id=instructor.instructor_id,
        instructor_name=instructor.instructor_name,
        instructor_bio=instructor.instructor_bio,
        instructor_specialty=instructor.instructor_specialty
    )

def student_interest_model_to_schema(student_interest: models.StudentInterest) -> StudentInterestSchema:
    return StudentInterestSchema(
        id=student_interest.id,
        student_id=student_interest.student_id,  # Mengganti "user_id" menjadi "student_id"
        interest=student_interest.interest
    )

import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request
import json
from fastapi.encoders import jsonable_encoder
class User:
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

json_filename="user.json"

with open(json_filename, "r") as read_file:
    data = json.load(read_file)

def write_data(data):
    with open(json_filename, "w") as write_file:
        json.dump(data, write_file, indent=4)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
app = FastAPI()
JWT_SECRET = 'myjwtsecret'
ALGORITHM = 'HS256'

authentication = APIRouter(tags=["Authentication"])

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

app.include_router(authentication)