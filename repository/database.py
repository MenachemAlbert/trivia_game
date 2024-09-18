import psycopg2
from psycopg2.extras import RealDictCursor
from config.sql_config import SQL_URI


def get_db_connection():
    return psycopg2.connect(SQL_URI, cursor_factory=RealDictCursor)


def create_tables():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                       CREATE TABLE IF NOT EXISTS "users" (
                       id SERIAL PRIMARY KEY,
                       first VARCHAR(255) NOT NULL,
                       last VARCHAR(255) NOT NULL,
                       email VARCHAR(255) NOT NULL UNIQUE
                       )
                       """)

            cursor.execute("""
                       CREATE TABLE IF NOT EXISTS question (
                       id SERIAL PRIMARY KEY,
                       question_text TEXT NOT NULL,
                       correct_answer VARCHAR(255) NOT NULL
                       )
                       """)

            cursor.execute("""
                       CREATE TABLE IF NOT EXISTS answer (
                       id SERIAL PRIMARY KEY,
                       question_id INTEGER NOT NULL,
                       incorrect_answer VARCHAR(255) NOT NULL,
                       FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE
                       )
                       """)

            cursor.execute("""
                       CREATE TABLE IF NOT EXISTS user_answer (
                       id SERIAL PRIMARY KEY,
                       user_id INTEGER NOT NULL,
                       question_id INTEGER NOT NULL,
                       answer_text VARCHAR(255) NOT NULL,
                       is_correct BOOLEAN NOT NULL,
                       time_taken INTEGER NOT NULL,
                       FOREIGN KEY (user_id) REFERENCES "users"(id) ON DELETE CASCADE,
                       FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE
                       )
                       """)
            connection.commit()
