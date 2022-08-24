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
            print(self.rightAnswer)
            self.operand = 'times'
        if(operator == 'division'):
            num1 = find_evenly_divisible(num1, num2)
            num2 = makeNum2Pos(num2)
            self.rightAnswer = round(num1/num2)
            self.operand = 'divided by'
        self.question = 'What is the result ' + \
            ' of ' + str(num1) + ' ' + self.operand + ' ' + str(num2) + '?'
        self.answerChoices = AnswerChoices(self.rightAnswer, operator)

# if num2 is 0, this function will return a non zero value
# necessary because we cannot divide by 0 (undefined)


def makeNum2Pos(num2):
    while(num2 == 0):
        num2 = random.randrange(-25, 25)
    return num2


def find_evenly_divisible(num1, num2):

    if(num1 % num2 != 0):
        num1 = num2 * random.randint(1, 25)
    return num1


class AnswerChoices:
    def __init__(self, rightAnswer, operator):

        # if(operator == 'division'):
        #     if(random1 != rightAnswer and random2 != rightAnswer and random3 != rightAnswer):
        #         if(random1 != random2 and random2 != random3 and random1 != random3):
        #             if(random1 != 0 and random2 != 0 and random3 != 0):
        #                 self.answerChoice1 = random1/random2
        #                 self.answerChoice2 = random2/random3
        #                 self.answerChoice3 = rightAnswer
        #                 self.answerChoice4 = random3/random1

        # if(operator != 'division'):
        random1 = random.randrange(rightAnswer-10, rightAnswer+10)
        random2 = random.randrange(rightAnswer-10, rightAnswer+10)
        random3 = random.randrange(rightAnswer-10, rightAnswer+10)
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
        randomNum1 = random.randint(-25, 25)
        randomNum2 = random.randint(-25, 25)
        indivQuestion = Question(operation, randomNum1, randomNum2)
        allQuestions.append(indivQuestion)

    return allQuestions
