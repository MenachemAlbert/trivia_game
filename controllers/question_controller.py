from dataclasses import asdict

from flask import Blueprint, jsonify, abort, request

from models.Question import Question
from models.User import User
from repository.question_repository import find_all_questions, find_question_by_id, create_question, delete_question, \
    update_question

question_blueprint = Blueprint("question", __name__)


@question_blueprint.route("/", methods=['GET'])
def get_all():
    questions = list(map(asdict, find_all_questions()))
    return jsonify(questions), 200


@question_blueprint.route("/<int:id_question>", methods=['GET'])
def get_question(id_question):
    question = find_question_by_id(id_question)
    if question:
        return jsonify(asdict(question)), 200
    else:
        return abort(404, description="Question not found")


@question_blueprint.route("/", methods=['POST'])
def create_new_question():
    data = request.json
    if not data or not all(k in data for k in ("question_text", "correct_answer")):
        return abort(400, description="Invalid data")
    question = Question(question_text=data["question_text"], correct_answer=data["correct_answer"])
    new_id = create_question(question)
    return jsonify({"id": new_id}), 201


@question_blueprint.route("/<int:id_question>", methods=['DELETE'])
def delete_existing_question(id_question):
    question = find_question_by_id(id_question)
    if not question:
        return abort(404, description="Question not found")
    delete_question(id_question)
    return '', 204


@question_blueprint.route("/<int:id_question>", methods=['PUT'])
def update_existing_question(id_question):
    question = find_question_by_id(id_question)
    if not question:
        return abort(404, description="Question not found")
    data = request.json
    if not data or not all(k in data for k in ("question_text", "correct_answer")):
        return abort(400, description="Invalid data")
    question.question_text = data["question_text"]
    question.correct_answer = data["correct_answer"]
    updated_question = update_question(question)
    return jsonify(asdict(updated_question)), 200
