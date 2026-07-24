from typing import Optional

from fastapi import (
    FastAPI,
    Depends,
    BackgroundTasks,
    Response,
    status
)

from fastapi.responses import JSONResponse

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base, engine, get_db
from models import Course, Student, Enrollment
from schemas import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    StudentCreate,
    StudentResponse,
    EnrollmentCreate,
    EnrollmentResponse,
)

app = FastAPI(
    title="Course Management REST API",
    description="RESTful API Design Best Practices - Hands-On 8",
    version="1.0"
)


# ---------------------------------------------------
# Create Database Tables
# ---------------------------------------------------

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "REST API Running Successfully"}


# ---------------------------------------------------
# STANDARD ERROR RESPONSE
# ---------------------------------------------------

def error_response(
    code: str,
    message: str,
    field: Optional[str] = None,
    status_code: int = 404
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


# ---------------------------------------------------
# API VERSIONING
#
# URL Versioning:
# /api/v1/courses/
#
# Alternative:
# Header Versioning
# Accept: application/vnd.api+json;version=1
# ---------------------------------------------------


# ===================================================
# COURSES
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


@app.get(
    "/api/v1/courses/",
    tags=["Courses"]
)
async def get_courses(
    page: int = 1,
    page_size: int = 2,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):

    query = select(Course)

    if search:

        query = query.where(

            or_(

                Course.name.ilike(f"%{search}%"),

                Course.code.ilike(f"%{search}%")

            )

        )

    total = await db.scalar(
        select(func.count()).select_from(query.subquery())
    )

    offset = (page - 1) * page_size

    result = await db.execute(
        query.offset(offset).limit(page_size)
    )

    courses = result.scalars().all()

    next_page = None
    previous_page = None

    if offset + page_size < total:
        next_page = (
            f"/api/v1/courses/?page={page+1}&page_size={page_size}"
        )

    if page > 1:
        previous_page = (
            f"/api/v1/courses/?page={page-1}&page_size={page_size}"
        )

    return {
        "count": total,
        "next": next_page,
        "previous": previous_page,
        "results": courses
    }


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
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if not course:
        return error_response(
            "NOT_FOUND",
            f"Course with id {course_id} does not exist"
        )

    return course


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
        select(Course).where(Course.id == course_id)
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
        select(Course).where(Course.id == course_id)
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
# DELETE COURSE
# ===================================================

@app.delete(
    "/api/v1/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"]
)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if not course:
        return error_response(
            "NOT_FOUND",
            f"Course with id {course_id} does not exist"
        )

    await db.delete(course)
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ===================================================
# STUDENTS
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
# COURSE -> STUDENTS (JOIN)
# ===================================================

@app.get(
    "/api/v1/courses/{course_id}/students/",
    response_model=list[StudentResponse],
    tags=["Courses"]
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

    print(f"Confirmation Email sent to Student {student_id}")


# ===================================================
# ENROLLMENTS
# ===================================================

@app.post(
    "/api/v1/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"]
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    response: Response,
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

    return Response(status_code=status.HTTP_204_NO_CONTENT)