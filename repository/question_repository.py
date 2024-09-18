from typing import List

from models.Question import Question
from repository.database import get_db_connection
from service.api_service import get_questions_from_api


def seed_questions():
    all_question = find_all_questions()
    if all_question and len(all_question) > 0:
        return
    question_list = get_questions_from_api()
    list(map(lambda q: create_question(q), question_list))


def create_question(question: Question) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO question (question_text , correct_answer)
            VALUES (%s, %s) RETURNING id
        """, (question.question_text, question.correct_answer))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id


def find_all_questions() -> List[Question]:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM question")
            res = cursor.fetchall()
            questions = [Question(**q) for q in res]
            return questions


def find_question_by_id(id_question: int) -> Question | None:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM question WHERE id = %s", (id_question,))
            res = cursor.fetchone()
            if res:
                return Question(**res)
            else:
                return None


def delete_question(id_question: int):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM question WHERE id = %s", (id_question,))
            connection.commit()


def update_question(question: Question) -> Question:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE question 
                SET question_text = %s, correct_answer = %s 
                WHERE id = %s
            """, (question.question_text, question.correct_answer, question.id))
            connection.commit()
    return question
