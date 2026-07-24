from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import Base, engine, get_db
from models import Department, Course, Student, Enrollment
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
    title="Course Management API",
    description="FastAPI CRUD API with Dependency Injection, Background Tasks and OpenAPI Documentation",
    version="1.0",
    contact={
        "name": "Kanisha",
        "email": "kanisha@example.com"
    }
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "API running"}


# ---------------------- COURSE CRUD ----------------------


@app.post(
    "/api/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create Course",
    response_description="Course Created Successfully",
)
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db)
):
    obj = Course(**course.dict())

    db.add(obj)

    await db.commit()
    await db.refresh(obj)

    return obj


@app.get(
    "/api/courses/",
    response_model=list[CourseResponse],
    tags=["Courses"]
)
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):

    stmt = select(Course)

    if department_id:
        stmt = stmt.where(Course.department_id == department_id)

    stmt = stmt.offset(skip).limit(limit)

    result = await db.execute(stmt)

    return result.scalars().all()


@app.get(
    "/api/courses/{course_id}",
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
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


@app.put(
    "/api/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def update_course(
    course_id: int,
    data: CourseUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    for key, value in data.dict(exclude_unset=True).items():
        setattr(course, key, value)

    await db.commit()
    await db.refresh(course)

    return course


@app.delete(
    "/api/courses/{course_id}",
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
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    await db.delete(course)
    await db.commit()

    return Response(status_code=204)
# ---------------------- STUDENTS ----------------------

@app.post(
    "/api/students/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"]
)
async def create_student(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db)
):
    obj = Student(**student.dict())

    db.add(obj)
    await db.commit()
    await db.refresh(obj)

    return obj


@app.get(
    "/api/students/",
    response_model=list[StudentResponse],
    tags=["Students"]
)
async def get_students(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(Student))

    return result.scalars().all()


# ---------------------- COURSE STUDENTS (JOIN) ----------------------

@app.get(
    "/api/courses/{course_id}/students/",
    tags=["Courses"]
)
async def get_course_students(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student)
        .join(Enrollment)
        .where(Enrollment.course_id == course_id)
    )

    return result.scalars().all()


# ---------------------- BACKGROUND TASK ----------------------

def send_confirmation_email(student_email: str):
    print(f"Sending confirmation to {student_email}")


# ---------------------- ENROLLMENTS ----------------------

@app.post(
    "/api/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"]
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):

    student = await db.get(Student, enrollment.student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    course = await db.get(Course, enrollment.course_id)

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    obj = Enrollment(**enrollment.dict())

    db.add(obj)

    await db.commit()
    await db.refresh(obj)

    background_tasks.add_task(
        send_confirmation_email,
        student.email
    )

    return obj


@app.get(
    "/api/enrollments/",
    response_model=list[EnrollmentResponse],
    tags=["Enrollments"]
)
async def get_enrollments(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(Enrollment))

    return result.scalars().all()


@app.delete(
    "/api/enrollments/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Enrollments"]
)
async def delete_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db)
):

    enrollment = await db.get(Enrollment, enrollment_id)

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    await db.delete(enrollment)
    await db.commit()

    return Response(status_code=204)