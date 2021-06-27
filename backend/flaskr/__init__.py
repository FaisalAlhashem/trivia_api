import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/trivia/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')

        return response

    def paginate_questions(request, questions):
        page = request.args.get('page', 1, type=int)
        start = (page-1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in questions]
        current_questions = questions[start:end]

        return current_questions

    @app.route('/categories', methods=['GET'])
    def get_categories():
        all_categories = Category.query.order_by(Category.id).all()
        categories = {}
        for category in all_categories:
            categories[str(category.id)] = category.type
        if len(categories) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'categories': categories
        })

    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def filter_questions(category_id):
        if category_id > '6' or category_id < '1':
            abort(404)

        questions = Question.query.filter(
            Question.category == category_id).all()
        current_questions = paginate_questions(request, questions)

        all_categories = Category.query.order_by(Category.id).all()
        categories = {}
        for category in all_categories:
            categories[category.id] = category.type
        if len(current_questions) == 0:
            abort(404)

        total_questions = len(Question.query.all())
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'category': categories,
            'current_category': category_id
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        all_categories = Category.query.order_by(Category.id).all()
        categories = {}
        for category in all_categories:
            categories[str(category.id)] = category.type
        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': 'all',
            'categories': categories
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()
        return jsonify({
            'success': True,
            'deleted': question_id
        })

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        try:
            searchTerm = body.get('searchTerm', None)
            if searchTerm is not None:
                questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(searchTerm)))

                current_questions = paginate_questions(request, questions)
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(questions.all())
                })
            else:
                questionText = body.get('question', None)
                answer = body.get('answer', None)
                difficulty = body.get('difficulty', None)
                category = body.get('category', None)
                if questionText is None or answer is None or difficulty is None or category is None:
                    abort(422)
                question = Question(
                    question=questionText,
                    answer=answer,
                    difficulty=difficulty,
                    category=category
                )

                question.insert()

                questions = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions': len(questions)
                })
        except:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def take_quiz():
        try:
            category = request.get_json().get('quiz_category')['id']
            if int(category) > 6 or int(category) < 0:
                abort(400)
            previous_questions = request.get_json().get('previous_questions')
            if category == 0:
                questions = Question.query.order_by(Question.id).all()
            else:
                questions = [question.format() for question in Question.query.filter(
                    Question.category == category).all()]
            for Qid in previous_questions:
                toBeDeleted = Question.query.filter(
                    Question.id == Qid).one_or_none()
                questions.remove(toBeDeleted.format())

            choice = None
            if len(questions) > 0:
                choice = random.choice(questions)
            return jsonify({
                'success': True,
                'previous_questions': previous_questions,
                'question': choice,
            })
        except:
            abort(400)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app
