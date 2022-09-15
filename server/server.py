import logging
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

description = """
A simple Math Quiz API that generates a 10 question Math Quiz based on what operation you use as a query parameter. ➕➖✖➗

# Operation

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

# socket_manager = SocketManager(app=app)

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
            self.operand = "+"
        if(operator == 'subtraction'):
            self.rightAnswer = num1 - num2
            self.operand = "-"
        if(operator == 'multiplication'):
            self.rightAnswer = num1 * num2
            print(self.rightAnswer)
            self.operand = "•"
        if(operator == 'division'):
            num2 = makeNum2Pos(num2)
            num1 = find_evenly_divisible(num1, num2)
            self.rightAnswer = round(num1/num2)
            self.operand = "÷"
        self.question = 'What is the result ' + \
            ' of ' + str(num1) + ' ' + self.operand + ' ' + str(num2) + '?'
        self.answerChoices = AnswerChoices(self.rightAnswer, operator)

# if num2 is 0, this function will return a non zero value
# necessary because we cannot divide by 0 (undefined)


# is the max number of people who can connect to a server at a time
LISTENER_LIMIT = 5
active_clients = []


def makeNum2Pos(num2):
    while(num2 == 0):
        num2 = random.randrange(-25, 25)
    return num2


def find_evenly_divisible(num1, num2):

    if(num1 % num2 != 0):
        num1 = num2 * random.randint(1, 25)
    return num1

# gets rid of repeat answer choices


def makeSureNotEqual(randnum1, randnum2, randnum3, rightAnswer):
    # for cases where at least one of the random numbers == rightAnswer
    # but are not equal to each othder
    while(randnum1 == rightAnswer or randnum2 == rightAnswer or randnum3 == rightAnswer):
        randnum1 = random.randrange(rightAnswer-15, rightAnswer+15)
        randnum2 = random.randrange(rightAnswer-15, rightAnswer+15)
        randnum3 = random.randrange(rightAnswer-15, rightAnswer+15)

    # if at least one set of randomnumbers are equal
    while(randnum1 == randnum2 or randnum2 == randnum3 or randnum1 == randnum3):
        randnum1 = random.randrange(rightAnswer-15, rightAnswer+15)
        randnum2 = random.randrange(rightAnswer-15, rightAnswer+15)
        randnum3 = random.randrange(rightAnswer-15, rightAnswer+15)
        # checks to see if any of the new numbers are equal to the right answer
        while(randnum1 == rightAnswer):
            randnum1 = random.randrange(rightAnswer-15, rightAnswer+15)

        while(randnum2 == rightAnswer):
            randnum2 = random.randrange(rightAnswer-15, rightAnswer+15)
        while(randnum3 == rightAnswer):
            randnum3 = random.randrange(rightAnswer-15, rightAnswer+15)

    listRandNums = [randnum1, randnum2, randnum3]
    return listRandNums


class AnswerChoices:
    def __init__(self, rightAnswer, operator):

        random1 = random.randrange(rightAnswer-15, rightAnswer+15)
        random2 = random.randrange(rightAnswer-15, rightAnswer+15)
        random3 = random.randrange(rightAnswer-15, rightAnswer+15)
        answerChoices = makeSureNotEqual(
            random1, random2, random3, rightAnswer)
        print(answerChoices)
        self.answerChoice1 = answerChoices[0]
        self.answerChoice2 = answerChoices[1]
        self.answerChoice3 = rightAnswer
        self.answerChoice4 = answerChoices[2]

        # need to have some negative answer choices


@app.get("/")
async def root():
    return "This API generates 10 questions for a Math quiz", 200


@app.get("/quiz")
async def createQuiz(operation: str = "addition"):
    allQuestions = []
    for x in range(0, 10):
        randomNum1 = random.randint(-25, 25)
        randomNum2 = random.randint(-25, 25)
        indivQuestion = Question(operation, randomNum1, randomNum2)
        allQuestions.append(indivQuestion)

    return allQuestions


# code for socketio
 
def handle_connect(sid, environ):
   print(f"Socket connected with sid {sid}")
# socket_handlers.py

# create a Socket.IO server
sio = socketio.AsyncServer()

# wrap with ASGI application
newapp = socketio.ASGIApp(sio)

# code for a user joining the socket (creating a socket)
# sid is our session id
@sio.event
def connect(sid, environ, auth):
    print('A user connected ', sid)
    sio.enter_room(sid, 'players')
    print('joined room')

@sio.event
def join_game(sid):
    sio.enter_room(sid, 'players')
    print('joined room')


@sio.event
def my_message(sid, data):
    sio.emit('room num', data, room='chat_users', skip_sid=sid)
# need an event to send all users a code when they create a socket
# this code is what other users will use to join same lobby





@sio.event
def disconnect(sid):
    print('disconnect ', sid)


# def begin_chat(sid):
#     print(sid)
#     sio.enter_room(sid, 'chat_users')
#     print('chat_users')
#     active_clients.append


# @sio.event
# def exit_chat(sid):
    
#     sio.leave_room(sid, 'chat_users')
