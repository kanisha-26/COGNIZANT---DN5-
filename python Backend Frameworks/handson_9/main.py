from datetime import timedelta

from fastapi import (
    FastAPI,
    Depends,
    Response,
    BackgroundTasks,
    status,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from database import Base, engine, get_db

from models import (
    Course,
    Student,
    Enrollment,
    User
)

from schemas import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    StudentCreate,
    StudentResponse,
    EnrollmentCreate,
    EnrollmentResponse,
    UserRegister,
    UserResponse,
    Token
)

from security import (
    get_password_hash,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)

app = FastAPI(
    title="Course Management API",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
@app.get("/")
async def root():
    return {"message": "Hands-On 9 API Running"}
def error_response(
    code,
    message,
    field=None,
    status_code=404
):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "field": field
            }
        }
    )
# ===================================================
# USER REGISTRATION
# ===================================================

@app.post(
    "/api/v1/auth/register/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"]
)
async def register_user(
    user: UserRegister,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User).where(User.email == user.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # bcrypt is preferred because it is intentionally slow,
    # making brute-force attacks much harder than MD5 or SHA-256.

    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_active=True
    )

    db.add(new_user)

    await db.commit()

    await db.refresh(new_user)

    return new_user
# ===================================================
# USER LOGIN
# ===================================================

@app.post(
    "/api/v1/auth/login/",
    response_model=Token,
    tags=["Authentication"]
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User).where(
            User.email == form_data.username
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
# ===================================================
# CREATE COURSE (Protected)
# ===================================================

@app.post(
    "/api/v1/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"]
)
async def create_course(
    course: CourseCreate,
    response: Response,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    new_course = Course(**course.dict())

    db.add(new_course)

    await db.commit()

    await db.refresh(new_course)

    response.headers["Location"] = (
        f"/api/v1/courses/{new_course.id}/"
    )

    return new_course
# ===================================================
# GET ALL COURSES
# ===================================================

@app.get(
    "/api/v1/courses/",
    response_model=list[CourseResponse],
    tags=["Courses"]
)
async def get_courses(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course)
    )

    return result.scalars().all()
# ===================================================
# GET COURSE BY ID
# ===================================================

@app.get(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if not course:
        return error_response(
            "NOT_FOUND",
            f"Course with id {course_id} does not exist"
        )

    return course
# ===================================================
# UPDATE COURSE
# ===================================================

@app.put(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def update_course(
    course_id: int,
    data: CourseCreate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if not course:
        return error_response(
            "NOT_FOUND",
            f"Course with id {course_id} does not exist"
        )

    course.name = data.name
    course.code = data.code
    course.credits = data.credits
    course.department_id = data.department_id

    await db.commit()

    await db.refresh(course)

    return course
# ===================================================
# PATCH COURSE
# ===================================================

@app.patch(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def patch_course(
    course_id: int,
    data: CourseUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if not course:
        return error_response(
            "NOT_FOUND",
            f"Course with id {course_id} does not exist"
        )

    for key, value in data.dict(exclude_unset=True).items():
        setattr(course, key, value)

    await db.commit()

    await db.refresh(course)

    return course
# ===================================================
# DELETE COURSE (Protected)
# ===================================================

@app.delete(
    "/api/v1/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"]
)
async def delete_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if not course:
        return error_response(
            "NOT_FOUND",
            f"Course with id {course_id} does not exist"
        )

    await db.delete(course)

    await db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
# ===================================================
# CREATE STUDENT
# ===================================================

@app.post(
    "/api/v1/students/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"]
)
async def create_student(
    student: StudentCreate,
    response: Response,
    db: AsyncSession = Depends(get_db)
):

    new_student = Student(**student.dict())

    db.add(new_student)

    await db.commit()

    await db.refresh(new_student)

    response.headers["Location"] = (
        f"/api/v1/students/{new_student.id}/"
    )

    return new_student


# ===================================================
# GET ALL STUDENTS
# ===================================================

@app.get(
    "/api/v1/students/",
    response_model=list[StudentResponse],
    tags=["Students"]
)
async def get_students(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student)
    )

    return result.scalars().all()


# ===================================================
# GET STUDENTS IN A COURSE (JOIN)
# ===================================================

@app.get(
    "/api/v1/courses/{course_id}/students/",
    response_model=list[StudentResponse],
    tags=["Students"]
)
async def get_students_in_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student)
        .join(Enrollment)
        .where(Enrollment.course_id == course_id)
    )

    return result.scalars().all()
# ===================================================
# BACKGROUND TASK
# ===================================================

def send_confirmation_email(student_id: int):
    print(f"Confirmation email sent to student {student_id}")


# ===================================================
# CREATE ENROLLMENT
# ===================================================

@app.post(
    "/api/v1/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"]
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    response: Response,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):

    new_enrollment = Enrollment(**enrollment.dict())

    db.add(new_enrollment)

    await db.commit()

    await db.refresh(new_enrollment)

    background_tasks.add_task(
        send_confirmation_email,
        new_enrollment.student_id
    )

    response.headers["Location"] = (
        f"/api/v1/enrollments/{new_enrollment.id}/"
    )

    return new_enrollment


# ===================================================
# GET ALL ENROLLMENTS
# ===================================================

@app.get(
    "/api/v1/enrollments/",
    response_model=list[EnrollmentResponse],
    tags=["Enrollments"]
)
async def get_enrollments(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Enrollment)
    )

    return result.scalars().all()


# ===================================================
# DELETE ENROLLMENT
# ===================================================

@app.delete(
    "/api/v1/enrollments/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Enrollments"]
)
async def delete_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    enrollment = result.scalar_one_or_none()

    if not enrollment:
        return error_response(
            "NOT_FOUND",
            f"Enrollment with id {enrollment_id} does not exist"
        )

    await db.delete(enrollment)

    await db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
