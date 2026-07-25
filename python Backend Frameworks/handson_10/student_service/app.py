from flask import Flask, request, jsonify
from database import db
from models import Student
import requests

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    return "Student Service Running"


# GET all students
@app.route("/api/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])


# CREATE student
@app.route("/api/students", methods=["POST"])
def create_student():
    data = request.get_json()

    student = Student(
        name=data["name"],
        email=data["email"]
    )

    db.session.add(student)
    db.session.commit()

    return jsonify(student.to_dict()), 201


# ENROLL STUDENT
@app.route("/api/students/<int:id>/enroll", methods=["POST"])
def enroll(id):

    student = Student.query.get(id)

    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.get_json()
    course_id = data["course_id"]

    try:
        response = requests.get(
            f"http://127.0.0.1:5001/api/courses/{course_id}"
        )

        if response.status_code != 200:
            return jsonify({"message": "Course not found"}), 404

    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Course Service Unavailable"}), 503

    return jsonify({"message": "Enrollment Successful"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(port=5002, debug=True)