import crud
from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import StudentSchema, ClassSchema, InstructorSchema, StudentInterestSchema, Request, Response, RequestStudent, RequestClass, RequestInstructor, RequestStudentInterest, student_model_to_schema, class_model_to_schema, instructor_model_to_schema, student_interest_model_to_schema
from typing import Annotated
from models import User
import requests

import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request
import json
from fastapi.encoders import jsonable_encoder

students = APIRouter()
instructors = APIRouter()
classes = APIRouter()
studentinterest = APIRouter()
recommendations = APIRouter()
authentication = APIRouter()
json_filename="user.json"

integratedToken = ''

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
    global integratedToken
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        print(f"Invalid username or password for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    url = 'https://bevbuddy--c3oinea.thankfulbush-47818fd3.southeastasia.azurecontainerapps.io/login'
    # url = 'http://localhost:8000/login'
    data = {
        'username': form_data.username,
        'password': form_data.password
    }
    response = requests.post(url, json=data)

    if response.status_code == 200:
        try:
            result = response.json()
            global integratedToken
            integratedToken = result.get('token')
            token = jwt.encode({'id': user.id, 'username': user.username}, JWT_SECRET, algorithm=ALGORITHM)
        except ValueError as e:
            print("Invalid JSON format in response:", response.text)
            return {'Error': 'Invalid JSON format in response'}
        return {'access_token': token, 'token_type': 'bearer', 'integrasiToken' : integratedToken}
    else:
        return {'Error': response.status_code, 'Detail': response.text}

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

@authentication.post('/user')
async def create_user(user_info: dict):
    username = user_info.get('username')
    fullname = user_info.get('fullname')
    password = user_info.get('password')
    email = user_info.get('email')

    if not username or not password or not fullname or not email:
        raise HTTPException(status_code=422, detail='All fields are required')

    for existing_user in data['user']:
        if existing_user['username'] == username:
            return {"error": "Username already taken"}

    last_user_id = data['user'][-1]['id'] if data['user'] else 0
    user_id = last_user_id + 1
    user = jsonable_encoder(User(id=user_id, username=username, password_hash=bcrypt.hash(password)))
    data['user'].append(user)

    url = 'https://bevbuddy--c3oinea.thankfulbush-47818fd3.southeastasia.azurecontainerapps.io/register'
    # url = 'http://localhost:8000/register'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    user_data = {
        "username": username,
        "fullname": fullname,
        "email": email + "@gmail.com",
        "password": password,
        "role": "customer",
        "token": "tokenmichael"
    }

    try:
        response = requests.post(url, headers=headers, json=user_data)
        response.raise_for_status()
        return {"username": username, "password": password, "email": email + "@gmail.com", "integratedRegister": response.json()}
    except requests.exceptions.RequestException as err:
        print(f"Error during request: {err}")
        return {"error": "An unexpected error occurred"}
    finally:
        write_data(data)

@authentication.get('/users/me')
async def get_user(user: User = Depends(get_current_user)):
    return {'id': user.id, 'username': user.username, 'role': 'admin'}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@students.post('/users')
async def create_user(username: str, fullname: str, password: str, email: str):
    for existing_user in data['user']:
        if existing_user['username'] == username:
            # Username already exists, return an appropriate response
            return {"error": "Username already taken"}

    last_user_id = data['user'][-1]['id'] if data['user'] else 0
    user_id = last_user_id + 1
    user = jsonable_encoder(User(id=user_id, username=username, password_hash=bcrypt.hash(password)))
    data['user'].append(user)

    url = 'https://bevbuddy--c3oinea.thankfulbush-47818fd3.southeastasia.azurecontainerapps.io/register'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    user_data = {
        "username": username,
        "fullname": fullname,
        "email": email + "@gmail.com",
        "password": password,
        "role": "customer",
        "token": "tokenmichael"
    }

    try:
        response = requests.post(url, headers=headers, json=user_data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return {"username": username, "password": password, "email": email + "@gmail.com", "integratedRegister": response.json()}
    except requests.exceptions.RequestException as err:
        print(f"Error during request: {err}")
        return {"error": "An unexpected error occurred"}
    finally:
        write_data(data)

@students.post("/students/create")
async def create_student_service(request: RequestStudent, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        student = crud.create_student(db, student=request.parameter)
        student_schema = student_model_to_schema(student)
        return Response(status="Ok", code="200", message="Student created successfully", result=student_schema)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@students.get("/students/")
async def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip, limit)
    student_schemas = [student_model_to_schema(student) for student in students]
    return Response(status="Ok", code="200", message="Success fetch all students", result=student_schemas)

@classes.post("/classes/create")
async def create_class_service(request: RequestClass, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        class_ = crud.create_class(db, class_=request.parameter)
        class_schema = class_model_to_schema(class_)
        return Response(status="Ok", code="200", message="Class created successfully", result=class_schema)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@classes.get("/classes/")
async def get_classes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    classes = crud.get_classes(db, skip, limit)
    class_schemas = [class_model_to_schema(class_) for class_ in classes]
    return Response(status="Ok", code="200", message="Success fetch all classes", result=class_schemas)

@instructors.post("/instructors/create")
async def create_instructor_service(request: RequestInstructor, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        instructor = crud.create_instructor(db, instructor=request.parameter)
        instructor_schema = instructor_model_to_schema(instructor)
        return Response(status="Ok", code="200", message="Instructor created successfully", result=instructor_schema)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@instructors.get("/instructors/")
async def get_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    instructors = crud.get_instructors(db, skip, limit)
    instructor_schemas = [instructor_model_to_schema(instructor) for instructor in instructors]
    return Response(status="Ok", code="200", message="Success fetch all instructors", result=instructor_schemas)

@studentinterest.post("/studentinterests/add")
async def add_student_interest_service(request: RequestStudentInterest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        student_id = request.parameter.student_id
        interest = request.parameter.interest
        crud.add_student_interest(db, student_id, interest)
        return Response(status="Ok", code="200", message="Interest added successfully", result=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@studentinterest.delete("/studentinterests/remove")
async def remove_student_interest_service(request: RequestStudentInterest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        student_id = request.parameter.student_id
        interest = request.parameter.interest
        crud.remove_student_interest(db, student_id, interest)
        return Response(status="Ok", code="200", message="Interest removed successfully", result=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_user_token(username: str, password: str):
    url = 'https://bevbuddy--c3oinea.thankfulbush-47818fd3.southeastasia.azurecontainerapps.io/login'
    data = {
        "username": "cilla567",
        "password": "cilla567"
    }
    response = requests.post(url, json=data)

    if response.status_code == 200:
        try:
            result = response.json()
            user_token = result.get('token')
            return user_token
        except ValueError as e:
            print("Invalid JSON format in response:", response.text)
            return None
    else:
        print(f"Failed to get token. Status code: {response.status_code}, Detail: {response.text}")
        return None

@recommendations.post("/recommendations")      
async def integrationrecommendations(request_data: dict):
    base_url = "https://bevbuddy--c3oinea.thankfulbush-47818fd3.southeastasia.azurecontainerapps.io/recommendations"
    username = "cilla567"
    password = "cilla567"
    token = get_user_token(username, password)
    
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.post(base_url, headers=headers, json=request_data)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
@recommendations.get("/classes/recommendations/{student_id}")
async def get_student_recommendations(student_id: int = Path(..., title="Student ID", description="The student's ID"), db: Session = Depends(get_db)):
    recommendations = crud.get_class_recommendations(db, student_id)
    class_schemas = [class_model_to_schema(class_) for class_ in recommendations]
    return Response(status="Ok", code="200", message="Recommendations based on student's interest", result=class_schemas)

@recommendations.get("/instructors/recommendations/{student_id}")
async def get_instructor_recommendations(student_id: int = Path(..., title="Student ID", description="The student's ID"), db: Session = Depends(get_db)):
    recommendations = crud.get_instructor_recommendations(db, student_id)
    instructor_schemas = [instructor_model_to_schema(instructor) for instructor in recommendations]
    return Response(status="Ok", code="200", message="Recommendations based on student's interest", result=instructor_schemas)

@classes.get("/students/classes/{student_id}")
async def get_classes_taken_by_student_service(student_id: int = Path(..., title="Student ID", description="The student's ID"), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    classes_taken = crud.get_classes_taken_by_student(db, student_id)
    class_schemas = [class_model_to_schema(class_) for class_ in classes_taken]
    return Response(status="Ok", code="200", message="Classes taken by the student", result=class_schemas)

@instructors.get("/students/instructors/{student_id}")
async def get_instructors_taught_by_student_service(student_id: int = Path(..., title="Student ID", description="The student's ID"), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    instructors_taught = crud.get_instructors_taught_by_student(db, student_id)
    instructor_schemas = [instructor_model_to_schema(instructor) for instructor in instructors_taught]
    return Response(status="Ok", code="200", message="Instructors taught by the student", result=instructor_schemas)

@classes.get("/classes/{class_id}")
async def get_class_info_service(class_id: int = Path(..., title="Class ID", description="The class's ID"), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    class_info = crud.get_class_info(db, class_id)
    if class_info:
        class_schema = class_model_to_schema(class_info)
        return Response(status="Ok", code="200", message="Class information", result=class_schema)
    else:
        raise HTTPException(status_code=404, detail="Class not found")

@instructors.get("/instructors/{instructor_id}")
async def get_instructor_info_service(instructor_id: int = Path(..., title="Instructor ID", description="The instructor's ID"), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    instructor_info = crud.get_instructor_info(db, instructor_id)
    if instructor_info:
        instructor_schema = instructor_model_to_schema(instructor_info)
        return Response(status="Ok", code="200", message="Instructor information", result=instructor_schema)
    else:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
from fastapi import Path, Body

@students.put("/students/update/{student_id}")
async def update_student_service(
    student_id: int = Path(..., title="Student ID", description="The student's ID"),
    updated_data: StudentSchema = Body(..., embed=True),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        crud.update_student(db, student_id, updated_data.dict(exclude_unset=True))
        return Response(status="Ok", code="200", message="Student updated successfully", result=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@students.patch("/students/update/{student_id}")
async def patch_student_service(
    student_id: int = Path(..., title="Student ID", description="The student's ID"),
    updated_data: StudentSchema = Body(..., embed=True),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        crud.update_student(db, student_id, updated_data.dict(exclude_unset=True))
        return Response(status="Ok", code="200", message="Student patched successfully", result=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@instructors.put("/instructors/update/{instructor_id}")
async def update_instructor_service(
    instructor_id: int = Path(..., title="Instructor ID", description="The instructor's ID"),
    updated_data: InstructorSchema = Body(..., embed=True),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        crud.update_instructor(db, instructor_id, updated_data.dict(exclude_unset=True))
        return Response(status="Ok", code="200", message="Instructor updated successfully", result=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@instructors.patch("/instructors/update/{instructor_id}")
async def patch_instructor_service(
    instructor_id: int = Path(..., title="Instructor ID", description="The instructor's ID"),
    updated_data: InstructorSchema = Body(..., embed=True),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        crud.update_instructor(db, instructor_id, updated_data.dict(exclude_unset=True))
        return Response(status="Ok", code="200", message="Instructor patched successfully", result=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")