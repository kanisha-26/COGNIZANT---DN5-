from pydantic import BaseModel, EmailStr
from typing import Optional


# ----------------------------------------------------
# DEPARTMENT
# ----------------------------------------------------

class DepartmentBase(BaseModel):
    name: str


class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


# ----------------------------------------------------
# COURSE
# ----------------------------------------------------

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


# ----------------------------------------------------
# STUDENT
# ----------------------------------------------------

class StudentCreate(BaseModel):
    name: str
    email: EmailStr


class StudentResponse(StudentCreate):
    id: int

    class Config:
        from_attributes = True


# ----------------------------------------------------
# ENROLLMENT
# ----------------------------------------------------

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(EnrollmentCreate):
    id: int

    class Config:
        from_attributes = True


# ----------------------------------------------------
# USER (Hands-On 9)
# ----------------------------------------------------

class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


# ----------------------------------------------------
# JWT TOKEN
# ----------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# ----------------------------------------------------
# DEPARTMENT WITH COURSES
# ----------------------------------------------------

class DepartmentWithCourses(DepartmentResponse):
    courses: list[CourseResponse] = []

    class Config:
        from_attributes = True