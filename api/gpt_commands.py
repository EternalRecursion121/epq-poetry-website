import openai
import dotenv
import os
import threading
import re

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

lock = threading.Lock()

def make_request(messages):
    if lock.acquire(blocking=False):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                max_tokens=350,
                
            )
            return response.choices[0]["message"]["content"]
        finally:
            lock.release()
    else:
        return "Another request is in progress, please try again later."

def feedback(poem):
    print(poem)
    if poem["themes"]:
        themes_str = "Themes: " + ", ".join(poem["themes"]) + "\n"
    else:
        themes_str = ""
    messages = [
        {"role": "system", "content":"You are CoPoetGPT, a helpful poetry assistant, designed to assist users in writing poetry. Your aim is to appreciate the strengths of the user's poetry, help them discover potential improvements they might have overlooked and to inspire their creative process rather than dictate it."},
        {"role": "user", "content": themes_str + f"{poem['name']}\n\n{poem['body']}\n\nPlease provide me some feedback on my poem."},
    ]
    return make_request(messages)

def generate_metaphor(poem, literal_thing, compared_to):
    if poem["themes"]:
        themes_str = "Themes: " + ", ".join(poem["themes"]) + "\n"
    else:
        themes_str = ""
    messages = [
        {"role": "system", "content": "You are CoPoetGPT, a creative assistant that can generate metaphors, while considering the context of a given poem. You should provide 5 distinct metaphors, and number each one for clarity."},
        {"role": "user", "content": themes_str + f"{poem['name']}\n\n{poem['body']}\n\nBased on this poem, can you generate five different metaphors comparing '{literal_thing}' to '{compared_to}', and please number each metaphor?"},
    ]
    response = make_request(messages)
    return re.split(r'\d\.', response)[1:]

def rewrite_line(poem, line):
    if poem["themes"]:
        themes_str = "Themes: " + ", ".join(poem["themes"]) + "\n"
    else:
        themes_str = ""
    messages = [
        {"role": "system", "content": "You are CoPoetGPT, a poetry assistant that can rewrite lines of a poem in a creative and poetic way. You should provide 5 distinct versions of a line from a poem, and number each one for clarity. Do not generate anything else."},
        {"role": "user", "content": themes_str + f"{poem['name']}\n\n{poem['body']}\n\nCan you provide me with five different rewrites for the line '{line}'?"},
    ]
    response = make_request(messages)
    return re.split(r'\d\.', response)[1:]

def generate_ideas(about):
    messages = [
        {"role": "system", "content":"You are CoPoetGPT, a creative poetry assistant designed to help users generate poetic ideas and themes. Your aim is to provide a variety of creative and insightful suggestions and ideas for writing a poem based on the given theme."},
        {"role": "user", "content":f"I would like to write a poem about {about}. Can you provide me with some creative ideas I could explore?"},
    ]
    return make_request(messages)