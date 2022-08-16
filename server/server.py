import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

description = """
A simple Math Quiz API that generates a 10 question Math Quiz based on what operation you use as a query parameter. ➕➖✖➗

## Operation

You can **read** a set of 10 quiz questions generated using the operation you passed in.
Parameters: addition, subtraction, multiplication, division


"""
app = FastAPI(
    title="MathQuizAPI",
    description=description,
    version="0.0.1",
    contact={
        "name": "Leah Thompson",
        "url": "https://leahthompson.netlify.app/",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question:
    def __init__(self, operator, num1, num2):
        if(operator == 'addition'):
            self.rightAnswer = num1 + num2
            self.operand = 'plus'
        if(operator == 'subtraction'):
            self.rightAnswer = num1 - num2
            self.operand = 'minus'
        if(operator == 'multiplication'):
            self.rightAnswer = num1 * num2
            self.operand = 'times'
        if(operator == 'division'):
            self.rightAnswer = round(num1 / num2, 1)
            self.operand = 'divided by'
        self.question = 'What is the result ' + \
            ' of ' + str(num1) + ' ' + self.operand + ' ' + str(num2) + '?'
        self.answerChoices = AnswerChoices(self.rightAnswer, operator)


class AnswerChoices:
    def __init__(self, rightAnswer, operator):
        if(operator == 'division'):
            random1 = random.randint(-100, 100)
            random2 = random.randint(-100, 100)
            random3 = random.randint(-100, 100)
            if(random1/random3 != rightAnswer and random2/random1 != rightAnswer and random3/random2 != rightAnswer):
                if(random1 != random2 and random2 != random3 and random1 != random3):
                    self.answerChoice1 = round(random1/random3, 1)
                    self.answerChoice2 = round(random2/random1, 1)
                    self.answerChoice3 = round(rightAnswer, 1)
                    self.answerChoice4 = round(random3/random2, 1)
        if(operator != 'division'):
            random1 = random.randint(-100, 100)
            random2 = random.randint(-100, 100)
            random3 = random.randint(-100, 100)
            if(random1 != rightAnswer and random2 != rightAnswer and random3 != rightAnswer):
                if(random1 != random2 and random2 != random3 and random1 != random3):
                    self.answerChoice1 = random1
                    self.answerChoice2 = random2
                    self.answerChoice3 = rightAnswer
                    self.answerChoice4 = random3
            # need to have some negative answer choices


@app.get("/")
async def root():
    return "This API generates 10 questions for a Math quiz", 200
#     # return {"message": "Connected to the API"}


@app.get("/quiz")
async def createQuiz(operation: str = "addition"):
    allQuestions = []
    for x in range(0, 10):
        randomNum1 = random.randint(-100, 100)
        randomNum2 = random.randint(-100, 100)
        indivQuestion = Question(operation, randomNum1, randomNum2)
        allQuestions.append(indivQuestion)

    return allQuestions
