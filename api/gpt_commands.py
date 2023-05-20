import openai
import dotenv
import os

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def feedback(poem):
    print(poem)
    if poem["themes"]:
        themes_str = "Themes: " + ", ".join(poem["themes"]) + "\n"
    else:
        themes_str = ""
    messages = [
        {"role": "system", "content":"You are CoPoetGPT, a helpful poetry assistant, designed to assist users in writing poetry. Your aim is to appreciate the strengths of the user's poetry, help them discover potential improvements they might have overlooked and to inspire their creative process rather than dictate it."},
        {"role": "user", "content": f"{poem['name']}\n" + themes_str + f"\n{poem['body']}\n\nPlease provide me some feedback on my poem."},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=350,
    )
    print(response)
    return response.choices[0]["message"]["content"]

def generate_metaphor(poem, literal_thing, compared_to):
    messages = [
        {"role": "system", "content": "You are CoPoetGPT, a creative assistant that can generate metaphors, while considering the context of a given poem."},
        {"role": "user", "content": f"{poem['name']}\nThemes: {poem['themes']}\n\n{poem['body']}\n\nBased on this poem, please generate 5 metaphors comparing '{literal_thing}' to '{compared_to}'"},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    return response.choices[0]["message"]["content"]

def rewrite_line(poem, line_index):
    lines = poem['body'].split("\n")
    if line_index < 0 or line_index >= len(lines):
        return "Invalid line index"
    target_line = lines[line_index]

    messages = [
        {"role": "system", "content": "You are CoPoetGPT, a poetry assistant that can rewrite lines of a poem in a creative and poetic way while maintaining its original meaning and tone."},
        {"role": "user", "content": f"{poem['title']}\nThemes: {poem['themes']}\n\n{poem['body']}\n\nCan you help me rewrite the line '{target_line}'?"},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=350,
    )
    return response.choices[0]["message"]["content"]