from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


openai_api_key = os.getenv('OPENAI_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')
serper_api_key = os.getenv('SERPER_API_KEY')
# openai_api_key = openai_api_key
# serper_api_key = serper_api_key

my_llm = ChatGroq(temperature=0, model_name="llama3-70b-8192",
                  groq_api_key=groq_api_key, )


search_tool = SerperDevTool()

researcher = Agent(
    role='Investigador principal',
    goal='Descubra tecnologías revolucionarias en {topic}',
    backstory="""Impulsado por la curiosidad, estás a la vanguardia de la innovación, deseosos de explorar y compartir conocimientos que podrían cambiar el mundo.""",
    # tools=None,
    llm=my_llm,
    function_calling_llm=my_llm,
    max_iter=3,
    max_rpm=10,
    verbose=True,
    memory=True,
    tools=[search_tool],
    allow_delegation=True,
)

writer = Agent(
    role='Escritor',
    goal='Narra historias tecnológicas convincentes sobre {topic}.',
    backstory="""Con un don para simplificar temas complejos, elaboras narraciones atractivas que cautivan y educan, sacando a la luz nuevos descubrimientos de forma accesible.""",
    # tools=None,
    llm=my_llm,
    function_calling_llm=my_llm,
    max_iter=3,
    max_rpm=10,
    verbose=True,
    memory=True,
    tools=[search_tool],
    allow_delegation=True,
)

research_task = Task(
    description=(
        """Identifica la próxima gran tendencia en {topic}. Céntrate en identificar los pros y los contras y la narrativa general. Su informe final debe articular claramente los puntos clave, sus oportunidades de mercado y los riesgos potenciales.
        """
    ),
    expected_output='Un completo informe de 3 párrafos sobre las últimas tendencias en {topic}.Entrega la respuesta en español.',
    tools=[search_tool],
    agent=researcher,
)

# Writing task with language model configuration
write_task = Task(
    description=(
        "Redacta un artículo perspicaz sobre {topic}."
        "Céntrate en las últimas tendencias y en cómo están afectando al sector."
        "Este artículo debe ser fácil de entender, atractivo y positivo."
    ),
    expected_output='Un artículo de 4 párrafos sobre {topic} avances formateado como markdown.',
    tools=[search_tool],
    agent=writer,
    async_execution=False,
    output_file='new-blog-post.md'  # Example of output customization
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # Optional: Sequential task execution is default
    memory=True,
    verbose=2,
    embedder={
        "provider": "openai",
        "config": {
                    "model": 'text-embedding-ada-002'
        }
    },
    max_rpm=10,
    share_crew=True
)

result = crew.kickoff(inputs={'topic': 'La IA en la sanidad'})
print(result)
