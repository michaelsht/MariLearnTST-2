import crud
from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import StudentSchema, ClassSchema, InstructorSchema, StudentInterestSchema, Request, Response, RequestStudent, RequestClass, RequestInstructor, RequestStudentInterest, student_model_to_schema, class_model_to_schema, instructor_model_to_schema, student_interest_model_to_schema
from typing import Annotated

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/students/create")
async def create_student_service(request: RequestStudent, db: Session = Depends(get_db)):
    try:
        student = crud.create_student(db, student=request.parameter)
        student_schema = student_model_to_schema(student)
        return Response(status="Ok", code="200", message="Student created successfully", result=student_schema)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/students/")
async def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip, limit)
    student_schemas = [student_model_to_schema(student) for student in students]
    return Response(status="Ok", code="200", message="Success fetch all students", result=student_schemas)

@router.post("/classes/create")
async def create_class_service(request: RequestClass, db: Session = Depends(get_db)):
    try:
        class_ = crud.create_class(db, class_=request.parameter)
        class_schema = class_model_to_schema(class_)
        return Response(status="Ok", code="200", message="Class created successfully", result=class_schema)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/classes/")
async def get_classes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    classes = crud.get_classes(db, skip, limit)
    class_schemas = [class_model_to_schema(class_) for class_ in classes]
    return Response(status="Ok", code="200", message="Success fetch all classes", result=class_schemas)

@router.post("/instructors/create")
async def create_instructor_service(request: RequestInstructor, db: Session = Depends(get_db)):
    try:
        instructor = crud.create_instructor(db, instructor=request.parameter)
        instructor_schema = instructor_model_to_schema(instructor)
        return Response(status="Ok", code="200", message="Instructor created successfully", result=instructor_schema)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/instructors/")
async def get_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    instructors = crud.get_instructors(db, skip, limit)
    instructor_schemas = [instructor_model_to_schema(instructor) for instructor in instructors]
    return Response(status="Ok", code="200", message="Success fetch all instructors", result=instructor_schemas)

@router.post("/studentinterests/add")
async def add_student_interest_service(request: RequestStudentInterest, db: Session = Depends(get_db)):
    try:
        student_id = request.parameter.student_id
        interest = request.parameter.interest
        crud.add_student_interest(db, student_id, interest)
        return Response(status="Ok", code="200", message="Interest added successfully", result=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/studentinterests/remove")
async def remove_student_interest_service(request: RequestStudentInterest, db: Session = Depends(get_db)):
    try:
        student_id = request.parameter.student_id
        interest = request.parameter.interest
        crud.remove_student_interest(db, student_id, interest)
        return Response(status="Ok", code="200", message="Interest removed successfully", result=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/students/recommendations/{student_id}")
async def get_student_recommendations(student_id: int = Path(..., title="Student ID", description="The student's ID"), db: Session = Depends(get_db)):
    recommendations = crud.get_class_recommendations(db, student_id)
    class_schemas = [class_model_to_schema(class_) for class_ in recommendations]
    return Response(status="Ok", code="200", message="Recommendations based on student's interest", result=class_schemas)

@router.get("/instructors/recommendations/{student_id}")
async def get_instructor_recommendations(student_id: int = Path(..., title="Student ID", description="The student's ID"), db: Session = Depends(get_db)):
    recommendations = crud.get_instructor_recommendations(db, student_id)
    instructor_schemas = [instructor_model_to_schema(instructor) for instructor in recommendations]
    return Response(status="Ok", code="200", message="Recommendations based on student's interest", result=instructor_schemas)
