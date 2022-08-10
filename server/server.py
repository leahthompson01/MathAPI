import random
from fastapi import FastAPI


app = FastAPI()


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
            self.rightAnswer = num1 / num2
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
                self.answerChoice1 = round(random1/random3, 1)
                self.answerChoice2 = round(random2/random1, 1)
                self.answerChoice3 = round(rightAnswer, 1)
                self.answerChoice4 = round(random3/random2, 1)
        if(operator != 'division'):
            random1 = random.randint(-100, 100)
            random2 = random.randint(-100, 100)
            random3 = random.randint(-100, 100)
            if(random1 != rightAnswer and random2 != rightAnswer and random3 != rightAnswer):
                self.answerChoice1 = random1
                self.answerChoice2 = random2
                self.answerChoice3 = rightAnswer
                self.answerChoice4 = random3
            # need to have some negative answer choices


@app.get("/")
async def root():
    return {"message": "Connected to the API"}


@app.get("/quiz")
async def createQuiz(operation: str = "addition"):
    print(operation)
    # if operation is None:
    #     operation = "addition"
    allQuestions = []
    for x in range(0, 10):
        randomNum1 = random.randint(-100, 100)
        randomNum2 = random.randint(-100, 100)
        indivQuestion = Question(operation, randomNum1, randomNum2)
        allQuestions.append(indivQuestion)

    return allQuestions
