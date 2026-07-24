from flask import Flask
from config import Config
from extensions import db, migrate
from courses.routes import courses_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(courses_bp)

    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not Found"}, 404

    @app.errorhandler(500)
    def server_error(error):
        return {"error": "Internal Server Error"}, 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)