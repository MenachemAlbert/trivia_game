from typing import List

from models.Answer import Answer
from repository.database import get_db_connection
from service.api_service import get_answers_from_api


def seed_answers():
    all_answers = find_all_answers()
    if all_answers and len(all_answers) > 0:
        return
    answers_list = get_answers_from_api()
    list(map(lambda a: create_answer(a), answers_list))


def create_answer(answer: Answer) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO answer (question_id , incorrect_answer)
            VALUES (%s, %s) RETURNING id
        """, (answer.question_id, answer.incorrect_answer))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id


def find_all_answers() -> List[Answer]:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM answer")
            res = cursor.fetchall()
            answers = [Answer(**a) for a in res]
            return answers


def find_answer_by_id(id_answer: int) -> Answer | None:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM answer WHERE id = %s", (id_answer,))
            res = cursor.fetchone()
            if res:
                return Answer(**res)
            else:
                return None


def delete_answer(id_answer: int):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM answer WHERE id = %s", (id_answer,))
            connection.commit()


def update_answer(answer: Answer) -> Answer:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE answer 
                SET question_id = %s, incorrect_answer = %s 
                WHERE id = %s
            """, (answer.question_id, answer.incorrect_answer, answer.id))
            connection.commit()
    return answer
