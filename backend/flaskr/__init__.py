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

    def paginate_questions(request, questions=[]):
        page = request.args.get('page', 1, type=int)
        start = (page-1) * QUESTIONS_PER_PAGE
        if len(questions) == 0:
            questions = Question.query.order_by(Question.id).limit(
                QUESTIONS_PER_PAGE).offset(start).all()
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in questions]
        # current_questions = questions[start:end]

        return questions

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
        CIDS = []  # array of every category ID
        all_categories = Category.query.order_by(Category.id).all()
        for category in all_categories:
            CIDS.append(category.id)
        try:
            CIDS.index(int(category_id))
        except ValueError as Value_error:
            print(Value_error)
            abort(404)
        questions = Question.query.filter(
            Question.category == category_id).all()
        current_questions = paginate_questions(request, questions)

        categories = {}
        for category in all_categories:
            categories[category.id] = category.type

        total_questions = len(current_questions)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'category': categories,
            'current_category': category_id
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        current_questions = paginate_questions(request)
        all_categories = Category.query.order_by(Category.id).all()
        categories = {}
        for category in all_categories:
            categories[str(category.id)] = category.type
        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': Question.query.count(),
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
                if not (questionText and answer and difficulty and category):
                    # since None is a falsy object it will trigger
                    raise ValueError(
                        'Some information is missing, unable to create question')
                question = Question(
                    question=questionText,
                    answer=answer,
                    difficulty=difficulty,
                    category=category
                )

                question.insert()

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'total_questions': Question.query.count()
                })
        except ValueError as Value_error:
            print(Value_error.with_traceback)
            abort(422)
        except Exception as e:
            print(e.with_traceback)
            abort(400)

    @app.route('/quizzes', methods=['POST'])
    def take_quiz():
        try:
            category_id = request.get_json().get('quiz_category')['id']
            CIDS = []  # array of every category ID
            all_categories = Category.query.order_by(Category.id).all()
            for category in all_categories:
                CIDS.append(category.id)
            CIDS.index(int(category_id))
            previous_questions = request.get_json().get('previous_questions')
            if category_id == 0:
                questions = Question.query.order_by(Question.id).all()
            else:
                unformated_questions = Question.query.filter(
                    Question.category == category_id).all()
                questions = [question.format()
                             for question in unformated_questions]
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
        except ValueError as Value_error:
            print(Value_error.with_traceback)
            abort(404)
        except Exception as e:
            print(e.with_traceback)
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
