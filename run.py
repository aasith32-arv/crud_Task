from flask import Flask
from sqlalchemy import text

from app.config import Config, db


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    db.init_app(flask_app)

    import app.models.course_model  # noqa: F401
    import app.models.student_model  # noqa: F401
    from app.routes.course_routes import course_bp
    from app.routes.student_routes import student_bp

    flask_app.register_blueprint(student_bp)
    flask_app.register_blueprint(course_bp)

    @flask_app.route('/')
    def home():
        return 'Hello World!'

    with flask_app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            print('Database connection successful!')
            db.create_all()
            print('Tables created successfully!')
        except Exception as e:
            print(f'Database error: {e}')

    return flask_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
