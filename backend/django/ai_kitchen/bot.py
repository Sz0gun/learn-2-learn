from openai import ask_assistant

def get_response(user_input):
    response = ask_assistant(user_input)
    return response