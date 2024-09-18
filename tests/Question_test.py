import pytest
from models.Question import Question
from repository.question_repository import (
    create_question,
    find_all_questions,
    find_question_by_id,
    update_question,
    delete_question
)


@pytest.fixture(scope="module")
def setup_questions():
    return find_all_questions()


def test_find_all_questions(setup_questions):
    questions = setup_questions
    assert len(questions) > 0, "No questions found in the database"


def test_create_question():
    new_question = Question(question_text=" try ", correct_answer=" try ")
    question_id = create_question(new_question)
    assert question_id is not None, "Failed to create a new question"


def test_find_question_by_id(setup_questions):
    question = setup_questions[0]
    found_question = find_question_by_id(question.id)
    assert found_question is not None, "Question not found by id"


def test_update_question():
    updated_question = Question(id=1, question_text=" try ", correct_answer=" try ")
    update_question(updated_question)
    question_after_update = find_question_by_id(1)
    assert question_after_update is not None, "Failed to update the question"


def test_delete_question():
    delete_question(1)
    deleted_question = find_question_by_id(1)
    assert deleted_question is None, "Question was not deleted"
