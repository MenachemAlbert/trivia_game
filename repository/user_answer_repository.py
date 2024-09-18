from typing import List
from datetime import timedelta
from models.UserAnswer import UserAnswer
from repository.database import get_db_connection


def create_user_answer(user_answer: UserAnswer) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO user_answer (user_id, question_id, answer_text, is_correct, time_taken)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """, (user_answer.user_id, user_answer.question_id, user_answer.answer_text,
              user_answer.is_correct, int(user_answer.time_taken.total_seconds())))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id


def find_all_user_answers() -> List[UserAnswer]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_answer")
        res = cursor.fetchall()
        user_answers = [
            UserAnswer(
                id=u['id'],
                user_id=u['user_id'],
                question_id=u['question_id'],
                answer_text=u['answer_text'],
                is_correct=u['is_correct'],
                time_taken=timedelta(seconds=u['time_taken'])
            ) for u in res
        ]
        return user_answers


def find_user_answer_by_id(id_user_answer: int) -> UserAnswer | None:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_answer WHERE id = %s", (id_user_answer,))
        res = cursor.fetchone()
        if res:
            return UserAnswer(
                id=res['id'],
                user_id=res['user_id'],
                question_id=res['question_id'],
                answer_text=res['answer_text'],
                is_correct=res['is_correct'],
                time_taken=timedelta(seconds=res['time_taken'])
            )
        else:
            return None


def delete_user_answer(id_user_answer: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM user_answer WHERE id = %s", (id_user_answer,))
        connection.commit()


def update_user_answer(user_answer: UserAnswer) -> UserAnswer:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            UPDATE user_answer 
            SET user_id = %s, question_id = %s, answer_text = %s, is_correct = %s, time_taken = %s
            WHERE id = %s
        """, (user_answer.user_id, user_answer.question_id, user_answer.answer_text,
              user_answer.is_correct, int(user_answer.time_taken.total_seconds()), user_answer.id))
        connection.commit()
    return user_answer
