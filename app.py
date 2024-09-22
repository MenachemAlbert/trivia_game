from controllers.question_controller import question_blueprint

from flask import Flask
from controllers.user_controller import user_blueprint
from service.main_service import initial_db

app = Flask(__name__)

if __name__ == '__main__':
    app.register_blueprint(user_blueprint, url_prefix="/api/users")
    app.register_blueprint(question_blueprint, url_prefix="/api/questions")

    initial_db()
    print("initial_db")

    app.run(debug=True)
