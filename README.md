# MariLearnTST

MariLearn is an EduTech-based service designed to provide learning opportunities for students to enhance their skills. This service is built on an API architecture, illustrated through various microservices.

## Endpoint URLs
- [Swagger Documentation](http://4.236.214.73/docs)

## File Structure
1. **config.py:** Application configuration file, including database connections and environment variables.
2. **crud.py:** CRUD module containing functions for entities such as students, classes, instructors, and student interests.
3. **dockerfile:** Dockerfile definition for running the application as a Docker container.
4. **main.py:** Main file serving as the entry point for FastAPI execution, including database table creation if not existing.
5. **models.py:** Models module with entity (model) definitions such as Student, Class, Instructor, and StudentInterest.
6. **requirements.txt:** File listing Python packages required by the application.
7. **routes.py:** Routes module containing API endpoint definitions and CRUD operations logic.
8. **schemas.py:** Schemas module with data schema definitions for API request and response validation.

## Routes
- **POST /token (Generate Token):**
  - Generates a JWT token based on the provided username and password.
  - Uses the `generate_token` function in the authentication module.

- **POST /users (Create User):**
  - Creates a new user with a username and password.
  - Uses the `create_user` function in the authentication module.

- **GET /users/me (Get Current User):**
  - Retrieves information about the current user (ID, username, and role).
  - Uses the `get_user` function in the authentication module.

- **POST /students/create (Create Student):**
  - Creates a new student with JSON data.
  - Calls `create_student` to add the student to the database.

- **GET /students/ (Get Students):**
  - Retrieves a list of students from the database.
  - Supports optional query parameters `skip` and `limit` for pagination.
  - Calls `get_students` to retrieve student data.

- **POST /classes/create (Create Class):**
  - Creates a new class with JSON data.
  - Calls `create_class` to add the class to the database.

- **GET /classes/ (Get Classes):**
  - Retrieves a list of classes from the database.
  - Supports optional query parameters `skip` and `limit` for pagination.
  - Calls `get_classes` to retrieve class data.

- **POST /instructors/create (Create Instructor):**
  - Creates a new instructor with JSON data.
  - Calls `create_instructor` to add the instructor to the database.

- **GET /instructors/ (Get Instructors):**
  - Retrieves a list of instructors from the database.
  - Supports optional query parameters `skip` and `limit` for pagination.
  - Calls `get_instructors` to retrieve instructor data.

- **POST /studentinterests/add (Add Student Interest):**
  - Adds an interest to a student's profile with JSON data.
  - Calls `add_student_interest` to add the interest to the student.

- **DELETE /studentinterests/remove (Remove Student Interest):**
  - Removes an interest from a student's profile with JSON data.
  - Calls `remove_student_interest` to remove the interest from the student.

- **GET /students/recommendations/{student_id} (Get Student Recommendations):**
  - Retrieves class recommendations for a student based on their interests.
  - Uses `student_id` as a path parameter.
  - Calls `get_class_recommendations` to retrieve class recommendations.

- **GET /instructors/recommendations/{student_id} (Get Instructor Recommendations):**
  - Retrieves instructor recommendations for a student based on their interests.
  - Uses `student_id` as a path parameter.
  - Calls `get_instructor_recommendations` to retrieve instructor recommendations.

## How to Run
1. Clone this repository.
2. Install dependencies by running `pip install -r requirements.txt`.
3. Run the application with the command `uvicorn main:app --reload`.

## How to Test
1. Open Swagger Documentation to view and test API endpoints.
2. Use the `/token` endpoint to generate a token by sending a username and password via Form Data.
3. Use the generated token to access the `/users/me` endpoint to get information about the current user.

## Docker Deployment
1. Build the Docker image with the command `docker build -t marilearn-auth-service ..`.
2. Run the Docker container with the command `docker run -p 80:80 marilearn-auth-service`.
