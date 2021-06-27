# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter) and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

> Once you're ready, you can submit your project on the last page.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [./backend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. _./backend/flaskr/`__init__.py`_
2. _./backend/test_flaskr.py_

### Frontend

The [./frontend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. _./frontend/src/components/QuestionView.js_
2. _./frontend/src/components/FormView.js_
3. _./frontend/src/components/QuizView.js_

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [README within ./frontend for more details.](./frontend/README.md)

## end points

in this api there are 3 end points in total those being

1. /questions
2. /categories
3. /quizzes

## /questions

GET /questions will return all questions regardless of category
while GET /category/<category_id>/questions will return all questions assosiated with the category id

POST /questions given a json item containing a 'searchTerm' will return all questions with the given search term in the question but if given a question, an answer , a difficulty and a category id it will create a new question

DELETE /questions/<question_id> will delete the question assosiated with the question_id

## /categories

GET /categories will return all categories and their IDs

## /quizzes

POST /quizzes if given an array of previous questions(left empty if its the first question) and a dictionary called quiz_category that has another dictionary that has the category id with a key called 'id'
it will return a random question that isn't from previous_questions and has the same category as 'id'
example of json:
json={
'previous_questions':[],
'quiz_category':{
'id':'1'
}
}
