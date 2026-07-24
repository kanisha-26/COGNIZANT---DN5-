from flask import Blueprint, request, jsonify
from extensions import db
from courses.models import Course, Enrollment

courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/courses"
)


@courses_bp.route("/", methods=["GET"])
def get_courses():

    courses = Course.query.all()

    return jsonify({
        "status": "success",
        "data": [c.to_dict() for c in courses]
    })


@courses_bp.route("/", methods=["POST"])
def add_course():

    data = request.get_json()

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"],
        department_id=data.get("department_id")
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "status": "success",
        "data": course.to_dict()
    }), 201


@courses_bp.route("/<int:id>", methods=["GET"])
def get_course(id):

    course = Course.query.get_or_404(id)

    return jsonify({
        "status": "success",
        "data": course.to_dict()
    })


@courses_bp.route("/<int:id>", methods=["PUT"])
def update_course(id):

    course = Course.query.get_or_404(id)

    data = request.get_json()

    course.name = data["name"]
    course.code = data["code"]
    course.credits = data["credits"]

    db.session.commit()

    return jsonify({
        "status": "success",
        "data": course.to_dict()
    })


@courses_bp.route("/<int:id>", methods=["DELETE"])
def delete_course(id):

    course = Course.query.get_or_404(id)

    db.session.delete(course)
    db.session.commit()

    return "", 204


@courses_bp.route("/<int:id>/students/", methods=["GET"])
def get_students(id):

    enrollments = Enrollment.query.filter_by(course_id=id).all()

    students = [e.student.to_dict() for e in enrollments]

    return jsonify({
        "status": "success",
        "data": students
    })