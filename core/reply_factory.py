
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

def generate_bot_responses(message, session):
    bot_responses = []

    session["current_question_id"] = 0
    session.modified = True
    session.save()
    current_question_id = session.get("current_question_id", 0)
    print("current_question_id",current_question_id)

    if message == 'sendproblem':
        bot_responses.append(BOT_WELCOME_MESSAGE)
        bot_responses.append({"question":PYTHON_QUESTION_LIST[current_question_id]["question_text"],"options":PYTHON_QUESTION_LIST[current_question_id]["options"]})
        return bot_responses

    # if not current_question_id:
    #     bot_responses.append(BOT_WELCOME_MESSAGE)

    eval = record_current_answer(message, current_question_id, session)


    next_question, next_options, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append({"eval":eval,"next_question":next_question,"next_options":next_options})
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.modified = True
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    question=PYTHON_QUESTION_LIST[current_question_id]
    
    session["current_question_id"] = current_question_id
    session["answer"] = answer
    session.modified = True
    session.save()

    if question["answer"] == answer: 
        session["score"]=session.get("score",0)+1       
        return "Correct!"
    else:
        return "The correct answer is: " + question["answer"] + ". Try the next question."


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id < len(PYTHON_QUESTION_LIST) - 1:
        next_question_id = current_question_id + 1
        next_question = PYTHON_QUESTION_LIST[next_question_id]["question_text"]
        next_options=PYTHON_QUESTION_LIST[next_question_id]["options"]
        return next_question,next_options ,next_question_id
    else:
        # next_question_id=current_question_id%len(PYTHON_QUESTION_LIST)
        # next_question = PYTHON_QUESTION_LIST[next_question_id]["question_text"]
        return None,""


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    return f"Your Score is :: {session.get('score',0)}/{len(PYTHON_QUESTION_LIST)}"
