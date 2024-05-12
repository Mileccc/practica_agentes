import os
from dotenv import load_dotenv
from openai import OpenAI


openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key)


def openai(messages):
    system_message3 = "Eres un experto en codificación y resolución de problemas"
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message3},
            {"role": "user", "content": messages},
        ],
        temperature=0.3,
    )
    message_content = response.choices[0].message.content.strip()
    return message_content


print(openai("Hablame sobre los dinosaurios"))
