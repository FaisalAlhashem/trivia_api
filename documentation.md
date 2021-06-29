# Full Stack API Final Project

## Trivia API

this api was made as a project for udacity's Full-Stack nanodegree and is the 2nd project in the course

the project is about a REStful api made for the purpose of making trivia questions and taking trivia quizzes

this api can:

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer(in the front end).
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

a front end was also included for the api, the front is made using React

## how to use the API

### backend

to use the api without an interface, you need to first download all the needed modules in the requirements.txt file for the backend to run, i recommend using a virtual environment you can learn more about virtual environments here [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

after installing all the needed modules cd into the backend directory and run the command:
in bash/zsh
```
FLASK_APP=flaskr FLASK_ENV=development flask run
```

to start the server and be able to interact with the api using either curl or postman

#### end points

the api has 3 end points in total

1. /questions
2. /categories
3. /quizzes

##### /questions

GET /questions will return a list of paginated questions regardless of their category as well as a list of all categories

example:
```
curl -X GET http://127.0.0.1:5000/questions
```

result:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "all",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
   ],
  "success": true,
  "total_questions": 20
}
```

POST /questions: if given a json object with a question, answer , difficulty, and a category it will make a new question and add it to the db , but if given a searchTerm it will return all questions that contain the search term 

example:
```
curl -X POST -d '{"question":"test", "answer":"test", "difficulty":"1","category":"1"}' -H "Content-Type: application/json" http://127.0.0.1:5000/questions
```

if any of the question, answer , difficulty, or category info were missing you will get a 422 error 

example 2:
```
curl -X POST -d '{"searchTerm": "title" }' -H "Content-Type: application/json" http://127.0.0.1:5000/questions
```

response: 
```
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

DELETE /questions/<questions_id> deletes the question with the given id 

example: 
```
curl -X DELETE http://127.0.0.1:5000/questions/45
```

if given an id that doesn't exist it will return a 404 error 

#### /categories

GET /categories will return all categories 

example:
```
curl -X GET http://127.0.0.1:5000/categories
```

result:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

GET categories/<int:category_id>/questions will return all questions that are of the given category id

example:
```
curl -X GET http://127.0.0.1:5000/categories/2/questions
```

result:
```
{
  "category": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "2",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

#### /quizzes

POST /quizzes will return a random question if given a json object that contains a previous_questions array and a quiz_category dictionary with an id key and a category id(0 for all categories)

example:
```
curl -d '{"previous_questions": [21], "quiz_category": { "id" : 1 } }' -H "Content-Type: application/json" http://127.0.0.1:5000/quizzes
```

### frontend
in order to run the front end you need to first set it up

#### Installing Dependencies

1. **Installing Node and NPM**<br>
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**<br>
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```
npm install
```

after installing you should see a folder name node_modules in the frontend folder 
to run the frontend cd into the frontend folder and run:
```
npm start
```
it is set to run on port 3000 by default
