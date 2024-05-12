import anthropic
from openai import OpenAI
from groq import Groq
import os
from dotenv import load_dotenv
import tempfile
import webbrowser
from tqdm import tqdm

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
groq_api_key = os.getenv('GROQ_API_KEY')


anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
ollama_client = OpenAI(base_url='http://localhost:11434/v1', api_key='llama3')
openai_client = OpenAI(api_key=openai_api_key)
groq_client = client = Groq(api_key=groq_api_key)


def open_file(filepath):
    with open(filepath, 'r', encoding="utf-8") as infile:
        return infile.read()


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


def ollamacpp(model, messages):
    system_message = {"role": "user", "content": messages}

    if not isinstance(messages, list):
        messages = [{"role": "user", "content": messages}]
    else:
        messages = [{"role": "user", "content": msg}
                    if not isinstance(msg, dict) else msg for msg in messages]
    messages.insert(0, system_message)

    response = ollama_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3
    )

    message_content = response.choices[0].message.content.strip()
    return message_content


def claude3(messages):
    response = anthropic_client.messages.create(
        model="claude-3-haiku-20240307",
        messages=[{"role": "user", "content": messages}],
        max_tokens=700,
        system="Eres un experto en codificación y resolución de problemas",
        temperature=0.3,
    )

    message_content = response.content[0].text
    return message_content


def groq_llama70B(messages, system_message):
    response = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": messages},
        ],
        model="llama3-70b-8192",
        temperature=0.3,
        max_tokens=1024,
    )

    message_content = response.choices[0].message.content.strip()
    return message_content


def generate_html_response(full_response):
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 40px;
                color:#333;
            }}
            .container {{
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            pre {{
                background-color: #282a36;
                color: #f8f8f2;
                border-radius: 5px;
                border: 1px solid #ccc;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', Courier, monospace;
                overflow-x: auto;
                white-space: pre-wrap;
            }}
            h1 {{
                color: #2c3e50;
            }}
            p, ol {{
                line-height: 1.6;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Respuesta de Asesores AI</h1>
            <p>Esta sección contiene respuestas generadas dinámicamente a partir de varios modelos de IA procesados por <code>El Rey:</code>  
            <pre>{full_response}</pre>
        </div>
    </body>
    </html>
    '''

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding="utf-8") as temp_file:
        temp_file.write(html_content)
        webbrowser.open('file://' + temp_file.name)


def the_king(user_message):
    system_message = """Eres el rey de los programadores y solucionadores de problemas, sabio y experto, que da respuestas meditadas a las preguntas.
    
    Tienes 10 asesores que te ofrecen sus puntos de vista para ayudarte.
    
    Considera sus puntos de vista y consejos, pero en última instancia proporciona tu propia respuesta razonada al problema basándote en todo el contexto y los consejos. Si sus aportaciones le resultan útiles, no dude en mencionarlas en su respuesta.
    """

    models = {
        "wizardlm2": "Wizardlm2",
        "mistral": "Mistral 7B",
        "qwen:7b": "Qwen 7B",
        "phi3": "Phi3",
        "gemma": "Gemma 7B",
        "openchat": "OpenChat",
        "llama3-chatqa:8b": "llama3 chatqa 8B",
        "llama3": "llama3"
    }
    answers = {}
    tasks = [f"Consulting {name}" for name in models.values()]
    progress_bar = tqdm(tasks, desc="Gathering insights", unit="task")

    for model, name in models.items():
        progress_bar.set_description(f"Consultando a {name}")
        answers[name] = ollamacpp(model, user_message)
        progress_bar.update()

    progress_bar.set_description("Procesando consulta a OpenAi")
    answers["OpeneAI 3.5 Pessant"] = openai(user_message)
    progress_bar.update()

    progress_bar.set_description("Procesando consulta Claude3")
    answers["Claude3"] = claude3(user_message)
    progress_bar.update()

    peasant_answer = "\n\n".join(
        f"{name} ayudante: {advice}" for name, advice in answers.items())

    progress_bar.set_description("Recopilación de consejos de los ayudantes")

    king_prompt = f"{peasant_answer}\n\n{{Problema}}: {user_message}\n\nUtiliza las ideas de los asesores para crear un plan paso a paso que resuelva el problema.\n\n{{Idoma-salida}}:  Español.\n\n{{Formato-respuesta}}: La respuesta debe contener un bloque de codigo con la solucion completa y comentarios explicativos."
    progress_bar.set_description("El Rey está resolviendo el problema")
    king_answer = groq_llama70B(king_prompt, system_message)
    progress_bar.update()

    progress_bar.close()
    return king_answer


question = open_file("marbleproblem.txt")
html_response1 = the_king(question)
html_response2 = the_king(html_response1)
generate_html_response(html_response2)
