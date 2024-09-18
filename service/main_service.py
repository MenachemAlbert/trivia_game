from repository.answer_repository import seed_answers
from repository.database import create_tables
from repository.question_repository import seed_questions
from repository.user_repository import seed_users


def initial_db():
    create_tables()
    seed_users()
    seed_questions()
    seed_answers()