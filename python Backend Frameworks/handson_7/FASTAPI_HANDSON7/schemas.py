from pydantic import BaseModel
from typing import Optional, List


# ---------------- Department ----------------

class DepartmentBase(BaseModel):
    name: str


class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


# ---------------- Course ----------------

class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(CourseCreate):
    id: int

    class Config:
        from_attributes = True


# ---------------- Student ----------------

class StudentCreate(BaseModel):
    name: str
    email: str


class StudentResponse(StudentCreate):
    id: int

    class Config:
        from_attributes = True


# ---------------- Enrollment ----------------

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(EnrollmentCreate):
    id: int

    class Config:
        from_attributes = True


# Nested Department Response

class DepartmentWithCourses(BaseModel):
    id: int
    name: str
    courses: List[CourseResponse] = []

    class Config:
        from_attributes = True