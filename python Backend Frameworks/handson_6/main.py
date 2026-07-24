from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import Base,engine,get_db
from models import Course
from schemas import CourseCreate,CourseUpdate,CourseResponse

app=FastAPI(
    title="Course Management API",
    version="1.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message":"API running"}

@app.post("/api/courses/",response_model=CourseResponse)
async def create_course(course:CourseCreate,db:AsyncSession=Depends(get_db)):
    obj=Course(**course.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

@app.get("/api/courses/",response_model=list[CourseResponse])
async def get_courses(
    skip:int=0,
    limit:int=10,
    department_id:int|None=None,
    db:AsyncSession=Depends(get_db)
):

    stmt=select(Course)

    if department_id:
        stmt=stmt.where(Course.department_id==department_id)

    stmt=stmt.offset(skip).limit(limit)

    result=await db.execute(stmt)

    return result.scalars().all()

@app.get("/api/courses/{course_id}",response_model=CourseResponse)
async def get_course(course_id:int,db:AsyncSession=Depends(get_db)):

    result=await db.execute(
        select(Course).where(Course.id==course_id)
    )

    course=result.scalar_one_or_none()

    if not course:
        raise HTTPException(404,"Course not found")

    return course

@app.put("/api/courses/{course_id}",response_model=CourseResponse)
async def update_course(
    course_id:int,
    data:CourseUpdate,
    db:AsyncSession=Depends(get_db)
):

    result=await db.execute(
        select(Course).where(Course.id==course_id)
    )

    course=result.scalar_one_or_none()

    if not course:
        raise HTTPException(404,"Course not found")

    for k,v in data.dict(exclude_unset=True).items():
        setattr(course,k,v)

    await db.commit()
    await db.refresh(course)

    return course

@app.delete("/api/courses/{course_id}")
async def delete_course(course_id:int,db:AsyncSession=Depends(get_db)):

    result=await db.execute(
        select(Course).where(Course.id==course_id)
    )

    course=result.scalar_one_or_none()

    if not course:
        raise HTTPException(404,"Course not found")

    await db.delete(course)
    await db.commit()

    return {"message":"Deleted"}