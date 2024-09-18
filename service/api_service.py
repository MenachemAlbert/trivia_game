from typing import List

from api.trivia_api import get_all_trivia
from api.user_api import get_users
from models.Answer import Answer
from models.User import User
from models.Question import Question


def get_users_from_api() -> List[User]:
    users = get_users()
    return [User(
        first=u["name"]["first"],
        last=u["name"]["last"],
        email=u["email"]
    ) for u in users]


def get_questions_from_api() -> List[Question]:
    all_trivia = get_all_trivia()
    return [Question(
        question_text=q["question"],
        correct_answer=q["correct_answer"]
    ) for q in all_trivia]


def get_answers_from_api() -> List[Answer]:
    all_trivia = get_all_trivia()
    answers = []
    question_id = 1
    for q in all_trivia:
        incorrect_answers = q.get("incorrect_answers")
        for answer in incorrect_answers:
            answers.append(Answer(
                question_id=question_id,
                incorrect_answer=answer
            ))
        question_id += 1
    return answers
