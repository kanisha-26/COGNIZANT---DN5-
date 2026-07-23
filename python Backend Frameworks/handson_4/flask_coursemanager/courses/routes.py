from flask import Blueprint, jsonify, request

courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/courses"
)

courses = []


def make_response_json(data, status_code):
    return jsonify({
        "status": "success",
        "data": data
    }), status_code


# GET all courses
@courses_bp.route("/", methods=["GET"])
def get_courses():
    return make_response_json(courses, 200)


# POST a new course
@courses_bp.route("/", methods=["POST"])
def add_course():

    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    required = ["name", "code", "credits"]

    for field in required:
        if field not in data:
            return jsonify(
                {"error": f"{field} is required"}
            ), 400

    course = {
        "id": len(courses) + 1,
        "name": data["name"],
        "code": data["code"],
        "credits": data["credits"]
    }

    courses.append(course)

    return make_response_json(course, 201)


# GET a course by ID
@courses_bp.route("/<int:course_id>", methods=["GET"])
def get_course(course_id):

    for course in courses:
        if course["id"] == course_id:
            return make_response_json(course, 200)

    return jsonify({"error": "Course not found"}), 404


# UPDATE a course
@courses_bp.route("/<int:course_id>", methods=["PUT"])
def update_course(course_id):

    data = request.get_json()

    for course in courses:
        if course["id"] == course_id:
            course.update(data)
            return make_response_json(course, 200)

    return jsonify({"error": "Course not found"}), 404


# DELETE a course
@courses_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):

    for course in courses:
        if course["id"] == course_id:
            courses.remove(course)
            return "", 204

    return jsonify({"error": "Course not found"}), 404