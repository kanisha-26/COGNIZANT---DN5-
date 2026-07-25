from flask import Flask, request, jsonify
from database import db
from models import Course

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///courses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():
    return "Course Service Running"

# GET all courses
@app.route("/api/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])

# GET course by ID
@app.route("/api/courses/<int:id>", methods=["GET"])
def get_course(id):
    course = Course.query.get(id)

    if not course:
        return jsonify({"message": "Course not found"}), 404

    return jsonify(course.to_dict())

# CREATE course
@app.route("/api/courses", methods=["POST"])
def create_course():
    data = request.get_json()

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"]
    )

    db.session.add(course)
    db.session.commit()

    return jsonify(course.to_dict()), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(port=5001, debug=True)